from django.contrib import admin

from .models import EngagementDailyRollup, EngagementEvent


@admin.register(EngagementEvent)
class EngagementEventAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'event_type',
        'object_type',
        'object_label',
        'object_id',
        'path',
        'language_code',
    )
    list_filter = ('event_type', 'object_type', 'language_code', 'created_at')
    search_fields = ('object_id', 'object_label', 'path', 'session_key')
    readonly_fields = (
        'event_type',
        'object_type',
        'object_id',
        'object_label',
        'path',
        'language_code',
        'session_key',
        'metadata',
        'created_at',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Engagement events (read-only stream)'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(EngagementDailyRollup)
class EngagementDailyRollupAdmin(admin.ModelAdmin):
    list_display = ('day', 'event_type', 'object_type', 'object_id', 'count')
    list_filter = ('event_type', 'object_type', 'day')
    search_fields = ('object_id',)
    ordering = ('-day', 'event_type')
    readonly_fields = ('day', 'event_type', 'object_type', 'object_id', 'count')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
