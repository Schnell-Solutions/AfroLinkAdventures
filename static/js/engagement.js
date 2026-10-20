(() => {
    const ENDPOINT = (
        document.body?.dataset?.analyticsCollect
        || document.documentElement.dataset.analyticsCollect
        || '/analytics/collect/'
    );
    const QUEUE_FLUSH_MS = 800;
    const MAX_QUEUE = 20;

    const PACKAGE_PATH = /^\/(?:journeys|itineraries)\/([^/?#]+)\/?$/i;
    const EVENT_PATH = /^\/events\/([^/?#]+)\/?$/i;

    let queue = [];
    let flushTimer = null;

    const absolutePath = (href) => {
        try {
            const url = new URL(href, window.location.origin);
            if (url.origin !== window.location.origin) {
                return null;
            }
            return url.pathname;
        } catch (_err) {
            return null;
        }
    };

    const enqueue = (event) => {
        if (!event || !event.event_type) {
            return;
        }
        queue.push({
            event_type: String(event.event_type),
            object_type: event.object_type ? String(event.object_type) : '',
            object_id: event.object_id != null ? String(event.object_id) : '',
            object_label: event.object_label ? String(event.object_label).slice(0, 255) : '',
            path: event.path ? String(event.path).slice(0, 500) : window.location.pathname,
            metadata: event.metadata && typeof event.metadata === 'object' ? event.metadata : {},
        });
        if (queue.length >= MAX_QUEUE) {
            flush(true);
            return;
        }
        window.clearTimeout(flushTimer);
        flushTimer = window.setTimeout(() => flush(false), QUEUE_FLUSH_MS);
    };

    const flush = (useBeacon) => {
        window.clearTimeout(flushTimer);
        flushTimer = null;
        if (!queue.length) {
            return;
        }
        const events = queue.splice(0, MAX_QUEUE);
        const body = JSON.stringify({ events });

        try {
            if (useBeacon && navigator.sendBeacon) {
                const blob = new Blob([body], { type: 'application/json' });
                navigator.sendBeacon(ENDPOINT, blob);
                return;
            }
        } catch (_err) {
            // Fall through to fetch.
        }

        fetch(ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            body,
            credentials: 'same-origin',
            keepalive: true,
        }).catch(() => {
            // Analytics must never surface errors to the user.
        });
    };

    const track = (eventType, details = {}) => {
        enqueue({
            event_type: eventType,
            ...details,
        });
    };

    const trackFromAnchor = (anchor) => {
        if (!anchor || anchor.hasAttribute('data-track-ignore')) {
            return;
        }

        if (anchor.hasAttribute('data-track')) {
            track(anchor.getAttribute('data-track'), {
                object_type: anchor.getAttribute('data-track-type') || '',
                object_id: anchor.getAttribute('data-track-id') || '',
                object_label: anchor.getAttribute('data-track-label') || '',
                path: absolutePath(anchor.href) || window.location.pathname,
                metadata: {
                    href: anchor.getAttribute('href') || '',
                },
            });
            return;
        }

        if (anchor.matches('[data-promo-link]')) {
            const slide = anchor.closest('[data-promo-slide]');
            const promoId = slide ? (slide.dataset.promoId || '') : '';
            const isPackagePromo = String(promoId).startsWith('package-promo-');
            track('banner_click', {
                object_type: isPackagePromo ? 'package_promo' : 'banner',
                object_id: promoId,
                object_label: (
                    (slide && slide.querySelector('.promo-banner__title')
                        ? slide.querySelector('.promo-banner__title').textContent
                        : '') || ''
                ).trim().slice(0, 255),
                path: absolutePath(anchor.href) || '',
                metadata: {
                    href: anchor.getAttribute('href') || '',
                },
            });
            return;
        }

        const path = absolutePath(anchor.href);
        if (!path) {
            return;
        }

        let match = path.match(PACKAGE_PATH);
        if (match) {
            track('package_click', {
                object_type: 'package',
                object_id: match[1],
                object_label: (anchor.textContent || '').trim().slice(0, 255),
                path,
                metadata: { slug: match[1] },
            });
            return;
        }

        match = path.match(EVENT_PATH);
        if (match) {
            track('event_click', {
                object_type: 'event',
                object_id: match[1],
                object_label: (anchor.textContent || '').trim().slice(0, 255),
                path,
                metadata: { slug: match[1] },
            });
        }
    };

    document.addEventListener('click', (event) => {
        const anchor = event.target.closest('a[href]');
        if (!anchor) {
            return;
        }
        trackFromAnchor(anchor);
    }, true);

    window.addEventListener('pagehide', () => flush(true));
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            flush(true);
        }
    });

    window.AfroLinkAnalytics = {
        track,
        trackSearch(filters = {}, extras = {}) {
            const cleaned = {};
            Object.entries(filters || {}).forEach(([key, value]) => {
                if (value != null && String(value).trim() !== '') {
                    cleaned[key] = String(value).trim().slice(0, 200);
                }
            });
            if (!Object.keys(cleaned).length) {
                return;
            }
            track('search_query', {
                object_type: 'listing',
                object_id: extras.surface || window.location.pathname,
                object_label: extras.label || document.title || '',
                path: window.location.pathname,
                metadata: {
                    ...cleaned,
                    surface: extras.surface || window.location.pathname,
                    result_count: extras.result_count,
                },
            });
        },
        flush: () => flush(true),
    };
})();
