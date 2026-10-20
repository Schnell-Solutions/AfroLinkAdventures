"""Shared Django admin helpers for AfroLink Adventures."""

from django.http import HttpResponseRedirect
from django.urls import reverse


class PlaceholderAdminMixin:
    """Attach placeholder attributes to form widgets by field name."""

    field_placeholders = {}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        placeholder = self.field_placeholders.get(db_field.name)
        if formfield is not None and placeholder:
            formfield.widget.attrs.setdefault('placeholder', placeholder)
        return formfield


class ContinueEditingMixin:
    """
    After creating an object, stay on the change form so staff can keep
    adding inlines (days, gallery, promotions) without hunting the list again.
    """

    continue_after_add = True

    def response_add(self, request, obj, post_url_continue=None):
        if not self.continue_after_add:
            return super().response_add(request, obj, post_url_continue)
        if '_addanother' in request.POST:
            return super().response_add(request, obj, post_url_continue)
        if '_popup' in request.POST:
            return super().response_add(request, obj, post_url_continue)
        opts = self.model._meta
        return HttpResponseRedirect(
            reverse(
                f'admin:{opts.app_label}_{opts.model_name}_change',
                args=[obj.pk],
            )
        )


class SoftActiveListFilterMixin:
    """Default list filter includes is_active where the model has it."""

    def get_list_filter(self, request):
        filters = list(super().get_list_filter(request) or ())
        if (
            hasattr(self.model, 'is_active')
            and 'is_active' not in filters
        ):
            filters = ['is_active', *filters]
        return filters
