(() => {
    const panel = document.querySelector('[data-detail-cta-panel]');
    const bar = document.querySelector('[data-detail-cta-bar]');
    if (!panel || !bar) {
        return;
    }

    const mobileQuery = window.matchMedia('(max-width: 960px)');
    let observer = null;

    const setAway = (away) => {
        bar.classList.toggle('is-away', away);
        if (away) {
            bar.setAttribute('aria-hidden', 'true');
        } else {
            bar.removeAttribute('aria-hidden');
        }
    };

    const syncVisibility = () => {
        if (!mobileQuery.matches) {
            bar.hidden = true;
            setAway(false);
            if (observer) {
                observer.disconnect();
                observer = null;
            }
            return;
        }

        bar.hidden = false;

        if (observer) {
            return;
        }

        observer = new IntersectionObserver(
            (entries) => {
                const entry = entries[0];
                if (!entry || !mobileQuery.matches) {
                    return;
                }
                // Hide slim bar once the full in-flow panel is meaningfully on screen.
                setAway(entry.isIntersecting && entry.intersectionRatio >= 0.35);
            },
            {
                root: null,
                threshold: [0, 0.35, 0.6, 1],
                rootMargin: '0px 0px -8% 0px',
            },
        );
        observer.observe(panel);
    };

    const mirror = bar.querySelector('[data-detail-cta-mirror]');
    if (mirror) {
        mirror.addEventListener('click', () => {
            const target = panel.querySelector(
                'button.xp-cta__btn[type="submit"], button.journey-cta__btn[type="submit"], button.xp-cta__btn, a.journey-cta__btn, a.xp-cta__btn',
            );
            if (target) {
                target.click();
            }
        });
    }

    if (typeof mobileQuery.addEventListener === 'function') {
        mobileQuery.addEventListener('change', syncVisibility);
    } else if (typeof mobileQuery.addListener === 'function') {
        mobileQuery.addListener(syncVisibility);
    }

    syncVisibility();
})();
