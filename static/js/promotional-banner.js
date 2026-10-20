(() => {
    const root = document.querySelector('[data-promo-banner]');
    if (!root) {
        return;
    }

    const STORAGE_KEY = 'afrolink.promoBanner.dismissed';
    const rotateMs = Number(root.dataset.rotateMs || 7000);
    const slides = Array.from(root.querySelectorAll('[data-promo-slide]'));

    if (!slides.length) {
        root.hidden = true;
        return;
    }

    const readDismissed = () => {
        try {
            const raw = window.sessionStorage.getItem(STORAGE_KEY);
            const parsed = raw ? JSON.parse(raw) : [];
            return Array.isArray(parsed) ? parsed.map(String) : [];
        } catch (_err) {
            return [];
        }
    };

    const writeDismissed = (ids) => {
        try {
            window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
        } catch (_err) {
            // Ignore storage failures (private mode, quota, etc.).
        }
    };

    let dismissed = new Set(readDismissed());
    let visibleSlides = [];
    let index = 0;
    let timer = null;
    let paused = false;

    const refreshVisible = () => {
        visibleSlides = slides.filter((slide) => {
            const id = String(slide.dataset.promoId || '');
            const dismissible = slide.dataset.dismissible === 'true';
            return !(dismissible && dismissed.has(id));
        });
    };

    const hideAll = () => {
        slides.forEach((slide) => {
            slide.hidden = true;
            slide.classList.remove('is-active');
        });
    };

    const showSlide = (slide) => {
        hideAll();
        if (!slide) {
            root.hidden = true;
            return;
        }
        slide.hidden = false;
        // Force reflow so the enter animation can replay.
        void slide.offsetWidth;
        slide.classList.add('is-active');
        root.hidden = false;
    };

    const clearTimer = () => {
        if (timer) {
            window.clearInterval(timer);
            timer = null;
        }
    };

    const advance = () => {
        if (paused || visibleSlides.length < 2) {
            return;
        }
        index = (index + 1) % visibleSlides.length;
        showSlide(visibleSlides[index]);
    };

    const startRotation = () => {
        clearTimer();
        if (paused || visibleSlides.length < 2 || rotateMs <= 0) {
            return;
        }
        timer = window.setInterval(advance, rotateMs);
    };

    const render = () => {
        refreshVisible();
        if (!visibleSlides.length) {
            clearTimer();
            hideAll();
            root.hidden = true;
            return;
        }
        if (index >= visibleSlides.length) {
            index = 0;
        }
        showSlide(visibleSlides[index]);
        startRotation();
    };

    root.addEventListener('click', (event) => {
        const dismissBtn = event.target.closest('[data-promo-dismiss]');
        if (!dismissBtn) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();

        const slide = dismissBtn.closest('[data-promo-slide]');
        if (!slide || slide.dataset.dismissible !== 'true') {
            return;
        }

        const id = String(slide.dataset.promoId || '');
        if (!id) {
            return;
        }

        dismissed.add(id);
        writeDismissed(Array.from(dismissed));

        const current = visibleSlides[index];
        refreshVisible();
        if (!visibleSlides.length) {
            render();
            return;
        }
        if (current === slide) {
            index = index % visibleSlides.length;
        } else {
            index = Math.max(0, visibleSlides.indexOf(current));
        }
        render();
    });

    root.addEventListener('mouseenter', () => {
        paused = true;
        clearTimer();
    });

    root.addEventListener('mouseleave', () => {
        paused = false;
        startRotation();
    });

    root.addEventListener('focusin', () => {
        paused = true;
        clearTimer();
    });

    root.addEventListener('focusout', (event) => {
        if (root.contains(event.relatedTarget)) {
            return;
        }
        paused = false;
        startRotation();
    });

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearTimer();
        } else if (!paused) {
            startRotation();
        }
    });

    render();
})();
