(() => {
    const root = document.querySelector('[data-language-switcher]');
    if (!root) {
        return;
    }

    const form = root.querySelector('form');
    const input = root.querySelector('[data-language-input]');
    const trigger = root.querySelector('[data-language-trigger]');
    const label = root.querySelector('[data-language-label]');
    const menu = root.querySelector('[data-language-menu]');
    const options = Array.from(root.querySelectorAll('[data-language-option]'));
    const current = (root.dataset.currentLanguage || 'en').toLowerCase().slice(0, 2);

    if (!form || !input || !trigger || !menu) {
        return;
    }

    let submitting = false;

    const close = () => {
        root.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
    };

    const open = () => {
        root.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
    };

    trigger.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (root.classList.contains('is-open')) {
            close();
        } else {
            open();
        }
    });

    options.forEach((option) => {
        option.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();

            const nextLanguage = (option.dataset.languageOption || '').toLowerCase();
            if (!nextLanguage || nextLanguage === current || submitting) {
                close();
                return;
            }

            submitting = true;
            input.value = nextLanguage;

            if (label) {
                label.innerHTML = option.innerHTML;
            }

            options.forEach((item) => {
                const selected = item === option;
                item.classList.toggle('is-selected', selected);
                item.setAttribute('aria-selected', String(selected));
            });

            close();
            form.submit();
        });
    });

    document.addEventListener('click', (event) => {
        if (!root.contains(event.target)) {
            close();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            close();
        }
    });
})();
