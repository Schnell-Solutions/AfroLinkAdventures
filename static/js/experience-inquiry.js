(() => {
    const modal = document.querySelector('[data-experience-inquiry-modal]');
    if (!modal) {
        return;
    }

    const dialog = modal.querySelector('[data-experience-inquiry-dialog]');
    const form = modal.querySelector('[data-experience-inquiry-form]');
    const successPanel = modal.querySelector('[data-experience-inquiry-success]');
    const successMessage = modal.querySelector('[data-experience-inquiry-success-message]');
    const pageUrlInput = modal.querySelector('[data-experience-inquiry-page-url]');
    const contextInput = modal.querySelector('[data-experience-inquiry-context]');
    const submitBtn = modal.querySelector('[data-experience-inquiry-submit]');
    const formError = modal.querySelector('[data-form-error]');
    const nameField = modal.querySelector('[data-experience-inquiry-name]');
    const messageField = modal.querySelector('[data-experience-inquiry-message]');
    const emailField = modal.querySelector('[data-experience-inquiry-email]');

    let lastFocus = null;
    let submitting = false;

    const getCookie = (name) => {
        const cookies = document.cookie ? document.cookie.split(';') : [];
        for (const raw of cookies) {
            const cookie = raw.trim();
            if (cookie.startsWith(`${name}=`)) {
                return decodeURIComponent(cookie.slice(name.length + 1));
            }
        }
        return '';
    };

    const clearErrors = () => {
        modal.querySelectorAll('[data-field-error]').forEach((el) => {
            el.hidden = true;
            el.textContent = '';
        });
        modal.querySelectorAll('.inquiry-modal__field').forEach((field) => {
            field.classList.remove('is-invalid');
        });
        if (formError) {
            formError.hidden = true;
            formError.textContent = '';
        }
    };

    const showFieldError = (name, message) => {
        const errorEl = modal.querySelector(`[data-field-error="${name}"]`);
        const field = errorEl?.closest('.inquiry-modal__field');
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.hidden = false;
        }
        if (field) {
            field.classList.add('is-invalid');
        }
    };

    const showForm = () => {
        if (form) {
            form.hidden = false;
        }
        if (successPanel) {
            successPanel.hidden = true;
        }
    };

    const showSuccess = (message) => {
        if (form) {
            form.hidden = true;
        }
        if (successPanel) {
            successPanel.hidden = false;
        }
        if (successMessage) {
            successMessage.textContent = message;
        }
        if (typeof window.showToast === 'function') {
            window.showToast(message);
        }
    };

    const openModal = (opener = null) => {
        lastFocus = document.activeElement;
        clearErrors();
        showForm();
        if (pageUrlInput) {
            pageUrlInput.value = window.location.href;
        }
        if (contextInput) {
            contextInput.value = opener?.dataset?.inquiryContext || '';
        }
        if (messageField && opener?.dataset?.inquiryContext && !messageField.value.trim()) {
            messageField.value = `Looking for options related to: ${opener.dataset.inquiryContext}`;
        }
        modal.hidden = false;
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('inquiry-modal-open');
        window.requestAnimationFrame(() => {
            (nameField || messageField || dialog)?.focus();
        });
    };

    const closeModal = () => {
        modal.hidden = true;
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('inquiry-modal-open');
        if (form && !submitting) {
            form.reset();
            clearErrors();
            showForm();
        }
        if (lastFocus && typeof lastFocus.focus === 'function') {
            lastFocus.focus();
        }
    };

    const validateClient = () => {
        clearErrors();
        const errors = {};
        const fullName = (nameField?.value || '').trim();
        const message = (messageField?.value || '').trim();
        const email = (emailField?.value || '').trim();

        if (!fullName) {
            errors.full_name = 'Please enter your name.';
        }

        if (!message) {
            errors.message = 'Please tell us what you are looking for.';
        } else if (message.length < 10) {
            errors.message = 'Please share a little more detail (at least 10 characters).';
        }

        if (!email) {
            errors.email = 'Please enter your email address.';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            errors.email = 'Please enter a valid email address.';
        }

        Object.entries(errors).forEach(([name, text]) => showFieldError(name, text));
        return Object.keys(errors).length === 0;
    };

    document.addEventListener('click', (event) => {
        const opener = event.target.closest('[data-open-experience-inquiry]');
        if (opener) {
            event.preventDefault();
            openModal(opener);
            return;
        }

        const closer = event.target.closest('[data-experience-inquiry-close]');
        if (closer && modal.contains(closer)) {
            event.preventDefault();
            if (!submitting) {
                closeModal();
            }
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !modal.hidden && !submitting) {
            closeModal();
        }
    });

    form?.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (submitting || !validateClient()) {
            return;
        }

        submitting = true;
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.dataset.label = submitBtn.textContent;
            submitBtn.textContent = 'Sending…';
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') || form.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                    'X-Requested-With': 'XMLHttpRequest',
                    Accept: 'application/json',
                },
                body: new FormData(form),
                credentials: 'same-origin',
            });

            let data = {};
            try {
                data = await response.json();
            } catch (_err) {
                data = {};
            }

            if (!response.ok || !data.ok) {
                clearErrors();
                if (data.errors) {
                    Object.entries(data.errors).forEach(([name, text]) => {
                        showFieldError(name, text);
                    });
                }
                if (formError) {
                    formError.textContent =
                        data.message || 'Something went wrong. Please try again.';
                    formError.hidden = false;
                }
                return;
            }

            form.reset();
            showSuccess(
                data.message ||
                    'Thank you — we received your inquiry and will be in touch shortly.'
            );
        } catch (_err) {
            if (formError) {
                formError.textContent =
                    'Unable to send your inquiry right now. Please try again.';
                formError.hidden = false;
            }
        } finally {
            submitting = false;
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = submitBtn.dataset.label || 'Submit';
            }
        }
    });
})();
