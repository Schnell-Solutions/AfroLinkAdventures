(() => {
    const root = document.querySelector('[data-partner-logos]');
    if (!root) {
        return;
    }

    const INTERVAL_MS = Number(root.dataset.intervalMs || 10000);
    const FADE_MS = 280;
    const MIN_VISIBLE = 1;

    const sources = Array.from(root.children).filter((node) => (
        node.classList.contains('partner-logo-link') && node.querySelector('img')
    )).map((node) => node.cloneNode(true));

    if (!sources.length) {
        return;
    }

    let startIndex = 0;
    let visibleCount = 1;
    let slotWidths = sources.map(() => 0);
    let timer = null;
    let fadeTimer = null;
    let reducedMotion = false;
    let syncing = false;

    const readGap = () => {
        const styles = getComputedStyle(root);
        const gap = Number.parseFloat(styles.columnGap || styles.gap || '0');
        return Number.isFinite(gap) ? gap : 0;
    };

    const readFallbackSlotWidth = () => {
        const styles = getComputedStyle(root.closest('.partner-strip') || root);
        const maxWidth = Number.parseFloat(styles.getPropertyValue('--partner-logo-max-width'));
        return Number.isFinite(maxWidth) && maxWidth > 0 ? maxWidth : 140;
    };

    const measureSlotWidths = () => {
        // Measure inside the real strip so CSS variables / logo max sizes apply.
        const clones = sources.map((source) => source.cloneNode(true));
        root.replaceChildren(...clones);
        void root.offsetWidth;

        const fallback = readFallbackSlotWidth();
        slotWidths = clones.map((clone) => {
            const width = Math.ceil(clone.getBoundingClientRect().width);
            return width > 0 ? width : fallback;
        });
    };

    const countFitting = (start) => {
        const available = root.clientWidth;
        if (available <= 0) {
            return MIN_VISIBLE;
        }

        const gap = readGap();
        const fallback = readFallbackSlotWidth();
        let used = 0;
        let count = 0;

        for (let i = 0; i < sources.length; i += 1) {
            const width = slotWidths[(start + i) % sources.length] || fallback;
            const next = count === 0 ? width : used + gap + width;
            if (next > available + 0.5) {
                break;
            }
            used = next;
            count += 1;
        }

        return Math.max(MIN_VISIBLE, Math.min(count || MIN_VISIBLE, sources.length));
    };

    const windowItems = (start, count) => {
        const size = Math.min(count, sources.length);
        const items = [];
        for (let i = 0; i < size; i += 1) {
            items.push(sources[(start + i) % sources.length].cloneNode(true));
        }
        return items;
    };

    const paint = (animate) => {
        const next = windowItems(startIndex, visibleCount);
        if (!animate || reducedMotion) {
            root.replaceChildren(...next);
            root.classList.remove('is-fading');
            return;
        }

        root.classList.add('is-fading');
        window.clearTimeout(fadeTimer);
        fadeTimer = window.setTimeout(() => {
            root.replaceChildren(...next);
            root.classList.remove('is-fading');
        }, FADE_MS);
    };

    const stopTimer = () => {
        if (timer !== null) {
            window.clearInterval(timer);
            timer = null;
        }
    };

    const shouldRotate = () => (
        !reducedMotion
        && sources.length > visibleCount
        && document.visibilityState === 'visible'
    );

    const advance = () => {
        if (!shouldRotate()) {
            return;
        }
        startIndex = (startIndex + visibleCount) % sources.length;
        visibleCount = countFitting(startIndex);
        paint(true);
    };

    const startTimer = () => {
        stopTimer();
        if (!shouldRotate()) {
            return;
        }
        timer = window.setInterval(advance, INTERVAL_MS);
    };

    const sync = () => {
        if (syncing) {
            return;
        }
        syncing = true;

        try {
            measureSlotWidths();
            visibleCount = countFitting(startIndex);

            if (sources.length <= visibleCount) {
                startIndex = 0;
                visibleCount = sources.length;
                paint(false);
                root.classList.add('is-ready');
                stopTimer();
                return;
            }

            startIndex = startIndex % sources.length;
            paint(false);
            root.classList.add('is-ready');
            startTimer();
        } finally {
            // Allow layout to settle before accepting resize callbacks again.
            window.requestAnimationFrame(() => {
                syncing = false;
            });
        }
    };

    const whenImagesReady = () => {
        const images = sources.flatMap((node) => Array.from(node.querySelectorAll('img')));
        const pending = images.filter((img) => !img.complete);

        if (!pending.length) {
            sync();
            return;
        }

        let settled = false;
        const finish = () => {
            if (settled) {
                return;
            }
            settled = true;
            sync();
        };

        let remaining = pending.length;
        pending.forEach((img) => {
            const done = () => {
                remaining -= 1;
                if (remaining <= 0) {
                    finish();
                }
            };
            img.addEventListener('load', done, { once: true });
            img.addEventListener('error', done, { once: true });
        });

        window.setTimeout(finish, 1200);
    };

    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const syncMotion = () => {
        reducedMotion = motionQuery.matches;
        sync();
    };

    if (typeof motionQuery.addEventListener === 'function') {
        motionQuery.addEventListener('change', syncMotion);
    } else if (typeof motionQuery.addListener === 'function') {
        motionQuery.addListener(syncMotion);
    }

    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            startTimer();
        } else {
            stopTimer();
        }
    });

    let resizeTimer = null;
    const scheduleSync = () => {
        if (syncing) {
            return;
        }
        window.clearTimeout(resizeTimer);
        resizeTimer = window.setTimeout(sync, 120);
    };

    window.addEventListener('resize', scheduleSync);

    if (typeof ResizeObserver === 'function') {
        const observer = new ResizeObserver(scheduleSync);
        observer.observe(root);
        const strip = root.closest('.partner-strip');
        if (strip) {
            observer.observe(strip);
        }
    }

    reducedMotion = motionQuery.matches;
    whenImagesReady();
})();
