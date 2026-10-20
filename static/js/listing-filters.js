(() => {
    const DURATION_RANGES = {
        short: { min: null, max: 7 },
        medium: { min: 8, max: 12 },
        long: { min: 13, max: null },
    };

    const debounce = (fn, wait = 220) => {
        let timer;
        return (...args) => {
            window.clearTimeout(timer);
            timer = window.setTimeout(() => fn(...args), wait);
        };
    };

    const closeCustomSelect = (select) => {
        const trigger = select.querySelector('.custom-select__trigger');
        select.classList.remove('is-open');
        if (trigger) {
            trigger.setAttribute('aria-expanded', 'false');
        }
    };

    const closeAllCustomSelects = (root, exceptSelect = null) => {
        root.querySelectorAll('[data-custom-select]').forEach((select) => {
            if (select !== exceptSelect) {
                closeCustomSelect(select);
            }
        });
    };

    const readFilters = (form) => {
        const filters = {};
        form.querySelectorAll('[name]').forEach((field) => {
            if (field.disabled) {
                return;
            }
            filters[field.name] = (field.value || '').trim();
        });
        return filters;
    };

    const hasActiveFilters = (filters, sortCountsAsFilter = false) =>
        Object.entries(filters).some(([key, value]) => {
            if (!value) {
                return false;
            }
            if (key === 'sort' && !sortCountsAsFilter) {
                return false;
            }
            return true;
        });

    const matchesSearch = (item, query) => {
        if (!query) {
            return true;
        }
        const haystack = (item.dataset.search || item.textContent || '').toLowerCase();
        return haystack.includes(query.toLowerCase());
    };

    const dataAttr = (item, key) => {
        if (Object.prototype.hasOwnProperty.call(item.dataset, key)) {
            return item.dataset[key];
        }
        const camel = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
        return item.dataset[camel];
    };

    const matchesExact = (item, key, value) => {
        if (!value) {
            return true;
        }
        return (dataAttr(item, key) || '') === value;
    };

    const matchesIncludes = (item, key, value) => {
        if (!value) {
            return true;
        }
        const haystack = ` ${dataAttr(item, key) || ''} `;
        return haystack.includes(` ${value} `);
    };

    const matchesDuration = (item, value) => {
        if (!value) {
            return true;
        }
        const range = DURATION_RANGES[value];
        if (!range) {
            return true;
        }
        const days = Number(item.dataset.durationDays || item.dataset.duration || '');
        if (Number.isNaN(days)) {
            return false;
        }
        if (range.min !== null && days < range.min) {
            return false;
        }
        if (range.max !== null && days > range.max) {
            return false;
        }
        return true;
    };

    const matchesDateRange = (item, dateFrom, dateTo) => {
        if (!dateFrom && !dateTo) {
            return true;
        }
        if (item.dataset.recurring === 'true' || item.dataset.recurring === '1') {
            return true;
        }
        const dateValue = item.dataset.date || '';
        if (!dateValue) {
            return false;
        }
        if (dateFrom && dateValue < dateFrom) {
            return false;
        }
        if (dateTo && dateValue > dateTo) {
            return false;
        }
        return true;
    };

    const itemMatches = (item, filters) => {
        if (!matchesSearch(item, filters.q || filters.search || '')) {
            return false;
        }

        const exactKeys = [
            'region',
            'style',
            'championship',
            'category',
            'type',
            'big_five',
            'offer',
        ];
        for (const key of exactKeys) {
            if (!matchesExact(item, key, filters[key] || '')) {
                return false;
            }
        }

        if (!matchesIncludes(item, 'experience', filters.experience || '')) {
            return false;
        }

        if (!matchesDuration(item, filters.duration || '')) {
            return false;
        }

        if (!matchesDateRange(item, filters.date_from || '', filters.date_to || '')) {
            return false;
        }

        return true;
    };

    const sortValue = (item, key) => {
        if (key === 'price') {
            const num = Number(item.dataset.sortPrice || item.dataset.price || '');
            return Number.isNaN(num) ? Number.POSITIVE_INFINITY : num;
        }
        if (key === 'duration') {
            const num = Number(
                item.dataset.sortDuration
                || item.dataset.durationDays
                || item.dataset.duration
                || ''
            );
            return Number.isNaN(num) ? Number.POSITIVE_INFINITY : num;
        }
        if (key === 'date') {
            return item.dataset.sortDate || item.dataset.date || '';
        }
        return (item.dataset.sortTitle || item.dataset.title || '').toLowerCase();
    };

    const compareItems = (a, b, sort) => {
        if (sort === 'oldest') {
            return String(sortValue(a, 'date')).localeCompare(String(sortValue(b, 'date')));
        }
        if (sort === 'duration') {
            return sortValue(a, 'duration') - sortValue(b, 'duration');
        }
        if (sort === 'price_asc') {
            return sortValue(a, 'price') - sortValue(b, 'price');
        }
        if (sort === 'price_desc') {
            return sortValue(b, 'price') - sortValue(a, 'price');
        }
        // newest / recommended default
        if (sort === '' || sort === 'newest') {
            const dateA = String(sortValue(a, 'date'));
            const dateB = String(sortValue(b, 'date'));
            if (dateA || dateB) {
                return dateB.localeCompare(dateA);
            }
            const orderA = Number(a.dataset.sortOrder || a.dataset.order || 0);
            const orderB = Number(b.dataset.sortOrder || b.dataset.order || 0);
            if (orderA || orderB) {
                return orderA - orderB;
            }
        }
        return String(sortValue(a, 'title')).localeCompare(String(sortValue(b, 'title')));
    };

    const syncUrl = (form, filters) => {
        if (form.dataset.syncUrl === 'false') {
            return;
        }
        const url = new URL(window.location.href);
        const params = url.searchParams;
        [...params.keys()].forEach((key) => {
            if (key !== 'page') {
                params.delete(key);
            }
        });
        Object.entries(filters).forEach(([key, value]) => {
            if (value) {
                params.set(key, value);
            }
        });
        const next = `${url.pathname}${params.toString() ? `?${params}` : ''}${url.hash}`;
        window.history.replaceState({}, '', next);
    };

    const updateSummary = (summary, count, singular, plural) => {
        if (!summary) {
            return;
        }
        const template = count === 1
            ? (summary.dataset.singular || singular || '{count} result found')
            : (summary.dataset.plural || plural || '{count} results found');
        summary.textContent = template.replace('{count}', String(count));
    };

    const initListingFilter = (root) => {
        const form = root.matches('[data-listing-filter]')
            ? root
            : root.querySelector('[data-listing-filter]');
        if (!form) {
            return;
        }

        const scope = root.matches('[data-listing-root]')
            ? root
            : (form.closest('[data-listing-root]') || document);
        const items = Array.from(scope.querySelectorAll('[data-filter-item]'));
        const emptyState = scope.querySelector('[data-filter-empty]');
        const summary = scope.querySelector('[data-filter-summary]');
        const clearControls = Array.from(scope.querySelectorAll('[data-filter-clear], [data-filter-clear-btn]'));
        const featuredBlocks = Array.from(scope.querySelectorAll('[data-filter-featured]'));
        const sortCountsAsFilter = form.dataset.sortIsFilter === 'true';
        const grid = scope.querySelector('[data-filter-grid]');
        let lastTrackedSignature = '';
        let lastSortKey = null;

        const applyFilters = ({ trackSearch = false } = {}) => {
            const filters = readFilters(form);
            const active = hasActiveFilters(filters, sortCountsAsFilter);
            let visibleCount = 0;

            featuredBlocks.forEach((block) => {
                block.hidden = active;
            });

            items.forEach((item) => {
                const isSpotlight = item.dataset.isFeatured === 'true'
                    || item.dataset.isPromoted === 'true';
                const matches = itemMatches(item, filters);
                const hideAsSpotlightTwin = !active && isSpotlight && featuredBlocks.length > 0;
                item.hidden = !matches || hideAsSpotlightTwin;
                if (matches && !hideAsSpotlightTwin) {
                    visibleCount += 1;
                }
            });

            if (grid) {
                const sortKey = filters.sort || '';
                if (sortKey !== lastSortKey) {
                    const sorted = [...items].sort((a, b) =>
                        compareItems(a, b, sortKey)
                    );
                    sorted.forEach((item) => grid.appendChild(item));
                    lastSortKey = sortKey;
                }
            }

            if (summary) {
                summary.hidden = !active;
                updateSummary(summary, visibleCount);
            }

            clearControls.forEach((control) => {
                if (control.matches('[data-filter-clear]')) {
                    control.hidden = !active;
                }
            });

            if (emptyState) {
                if (!items.length) {
                    emptyState.hidden = false;
                } else {
                    emptyState.hidden = visibleCount > 0;
                }
            }

            syncUrl(form, filters);

            if (
                trackSearch
                && window.AfroLinkAnalytics
                && typeof window.AfroLinkAnalytics.trackSearch === 'function'
            ) {
                const searchable = { ...filters };
                delete searchable.sort;
                if (hasActiveFilters(searchable, false)) {
                    const signature = JSON.stringify(searchable);
                    if (signature !== lastTrackedSignature) {
                        lastTrackedSignature = signature;
                        window.AfroLinkAnalytics.trackSearch(searchable, {
                            surface: window.location.pathname,
                            result_count: visibleCount,
                            label: document.title || '',
                        });
                    }
                }
            }
        };

        const clearFilters = (event) => {
            if (event) {
                event.preventDefault();
            }
            form.querySelectorAll('[name]').forEach((field) => {
                field.value = '';
            });
            form.querySelectorAll('[data-custom-select]').forEach((select) => {
                const label = select.querySelector('[data-custom-select-label]');
                const options = select.querySelectorAll('.custom-select__option');
                const defaultOption = select.querySelector('.custom-select__option[data-value=""]')
                    || options[0];
                options.forEach((option) => {
                    const isSelected = option === defaultOption;
                    option.classList.toggle('is-selected', isSelected);
                    option.setAttribute('aria-selected', String(isSelected));
                });
                if (label && defaultOption) {
                    label.textContent = defaultOption.textContent.trim();
                }
            });
            applyFilters({ trackSearch: true });
        };

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            applyFilters({ trackSearch: true });
        });

        form.querySelectorAll('[data-custom-select]').forEach((select) => {
            const trigger = select.querySelector('.custom-select__trigger');
            const label = select.querySelector('[data-custom-select-label]');
            const input = select.querySelector('[data-custom-select-input]');
            const options = select.querySelectorAll('.custom-select__option');
            if (!trigger || !input) {
                return;
            }

            trigger.addEventListener('click', () => {
                const isOpen = select.classList.contains('is-open');
                closeAllCustomSelects(form, select);
                select.classList.toggle('is-open', !isOpen);
                trigger.setAttribute('aria-expanded', String(!isOpen));
            });

            options.forEach((option) => {
                option.addEventListener('click', () => {
                    input.value = option.dataset.value || '';
                    if (label) {
                        label.textContent = option.textContent.trim();
                    }
                    options.forEach((item) => {
                        const isSelected = item === option;
                        item.classList.toggle('is-selected', isSelected);
                        item.setAttribute('aria-selected', String(isSelected));
                    });
                    closeCustomSelect(select);
                    applyFilters({ trackSearch: true });
                });
            });

            select.addEventListener('keydown', (event) => {
                if (event.key === 'Escape') {
                    closeCustomSelect(select);
                    trigger.focus();
                }
            });
        });

        const debouncedApply = debounce(() => applyFilters({ trackSearch: true }));
        form.querySelectorAll('input[type="search"], input[name="q"], input[name="search"]').forEach((input) => {
            input.addEventListener('input', debouncedApply);
        });
        form.querySelectorAll('input[type="date"], [data-auto-filter-change]').forEach((input) => {
            input.addEventListener('change', () => applyFilters({ trackSearch: true }));
        });

        clearControls.forEach((control) => {
            control.addEventListener('click', clearFilters);
        });

        document.addEventListener('click', (event) => {
            if (!event.target.closest('[data-custom-select]')) {
                closeAllCustomSelects(form);
            }
        });

        applyFilters();
    };

    const initRegionFilter = (root) => {
        const searchInput = root.querySelector('[data-region-search]');
        const typeInput = root.querySelector('[data-region-type]');
        const select = root.querySelector('[data-region-select]');
        const items = Array.from(root.querySelectorAll('[data-filter-item], [data-region-grid] .content-card'));
        const emptyState = root.querySelector('[data-filter-empty]');

        if (!searchInput || !typeInput || !items.length) {
            return;
        }

        const applyFilters = ({ trackSearch = false } = {}) => {
            const activeType = typeInput.value || 'all';
            const query = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            items.forEach((card) => {
                const matchesType = activeType === 'all' || card.dataset.type === activeType;
                const matchesQuery = !query || (card.dataset.search || '').toLowerCase().includes(query);
                const visible = matchesType && matchesQuery;
                card.hidden = !visible;
                if (visible) {
                    visibleCount += 1;
                }
            });

            if (emptyState) {
                emptyState.hidden = visibleCount > 0;
            }

            if (
                trackSearch
                && (query || activeType !== 'all')
                && window.AfroLinkAnalytics
                && typeof window.AfroLinkAnalytics.trackSearch === 'function'
            ) {
                window.AfroLinkAnalytics.trackSearch(
                    {
                        q: query,
                        type: activeType !== 'all' ? activeType : '',
                    },
                    {
                        surface: window.location.pathname,
                        result_count: visibleCount,
                        label: document.title || '',
                    },
                );
            }
        };

        if (select) {
            const trigger = select.querySelector('.custom-select__trigger');
            const label = select.querySelector('[data-region-select-label]');
            const options = select.querySelectorAll('.custom-select__option');

            const closeSelect = () => {
                select.classList.remove('is-open');
                if (trigger) {
                    trigger.setAttribute('aria-expanded', 'false');
                }
            };

            if (trigger) {
                trigger.addEventListener('click', () => {
                    const isOpen = select.classList.contains('is-open');
                    select.classList.toggle('is-open', !isOpen);
                    trigger.setAttribute('aria-expanded', String(!isOpen));
                });
            }

            options.forEach((option) => {
                option.addEventListener('click', () => {
                    typeInput.value = option.dataset.value || 'all';
                    if (label) {
                        label.textContent = option.textContent.trim();
                    }
                    options.forEach((item) => {
                        const isSelected = item === option;
                        item.classList.toggle('is-selected', isSelected);
                        item.setAttribute('aria-selected', String(isSelected));
                    });
                    closeSelect();
                    applyFilters({ trackSearch: true });
                });
            });

            select.addEventListener('keydown', (event) => {
                if (event.key === 'Escape') {
                    closeSelect();
                    trigger?.focus();
                }
            });

            document.addEventListener('click', (event) => {
                if (!select.contains(event.target)) {
                    closeSelect();
                }
            });
        }

        const emptyClear = root.querySelector('[data-filter-clear-btn]');
        if (emptyClear) {
            emptyClear.addEventListener('click', (event) => {
                event.preventDefault();
                searchInput.value = '';
                typeInput.value = 'all';
                if (select) {
                    const label = select.querySelector('[data-region-select-label]');
                    const options = select.querySelectorAll('.custom-select__option');
                    const defaultOption = select.querySelector('.custom-select__option[data-value="all"]') || options[0];
                    options.forEach((option) => {
                        const isSelected = option === defaultOption;
                        option.classList.toggle('is-selected', isSelected);
                        option.setAttribute('aria-selected', String(isSelected));
                    });
                    if (label && defaultOption) {
                        label.textContent = defaultOption.textContent.trim();
                    }
                }
                applyFilters({ trackSearch: true });
            });
        }

        searchInput.addEventListener('input', debounce(() => applyFilters({ trackSearch: true }), 180));
        applyFilters();
    };

    document.querySelectorAll('[data-listing-root]').forEach((root) => {
        if (root.querySelector('[data-listing-filter]')) {
            initListingFilter(root);
        } else if (root.querySelector('[data-region-search]')) {
            initRegionFilter(root);
        }
    });
})();
