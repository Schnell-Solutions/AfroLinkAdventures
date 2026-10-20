from django.contrib import admin

from destination_cms.admin_mixins import ContinueEditingMixin, PlaceholderAdminMixin

from .models import (
    Consultation,
    ExperienceInquiry,
    Inquiry,
    InquiryCustomDay,
    InquiryInterest,
    InquiryPackage,
    Lead,
)


class InquiryInline(admin.TabularInline):
    model = Inquiry
    extra = 0
    show_change_link = True
    fields = (
        'inquiry_type',
        'status',
        'guest_count',
        'target_start_date',
        'accommodation_tier',
        'created_at',
    )
    readonly_fields = ('created_at',)
    verbose_name_plural = (
        'Inquiries — use the change link on a row to manage packages & consultation'
    )


class InquiryPackageInline(admin.TabularInline):
    model = InquiryPackage
    extra = 0
    autocomplete_fields = ('base_package',)
    verbose_name_plural = 'Requested journey packages'


class InquiryInterestInline(admin.TabularInline):
    model = InquiryInterest
    extra = 0
    fields = ('interest_type', 'title_snapshot', 'notes', 'created_at')
    readonly_fields = ('created_at',)
    verbose_name_plural = 'Shortlisted experiences / events'


class InquiryCustomDayInline(admin.TabularInline):
    model = InquiryCustomDay
    extra = 0
    autocomplete_fields = ('region', 'golf_course', 'safari_extension')
    verbose_name_plural = 'Custom planner days'


class ConsultationInline(admin.TabularInline):
    model = Consultation
    extra = 0
    fields = ('scheduled_time', 'status', 'meeting_url')
    verbose_name_plural = 'Consultations — meeting URL optional until confirmed'


@admin.register(Lead)
class LeadAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        'full_name',
        'email',
        'phone',
        'preferred_contact',
        'budget_band',
        'trip_flexibility',
        'preferred_language',
        'inquiry_status',
        'assigned_to',
        'created_at',
    )
    list_filter = (
        'preferred_language',
        'preferred_contact',
        'budget_band',
        'trip_flexibility',
        'inquiry_status',
        'assigned_to',
        'created_at',
    )
    list_editable = ('inquiry_status',)
    search_fields = ('full_name', 'email', 'phone', 'notes', 'planning_focus')
    autocomplete_fields = ('assigned_to',)
    inlines = [InquiryInline]
    save_on_top = True
    field_placeholders = {
        'full_name': 'Guest full name',
        'email': 'guest@email.com',
        'phone': '+254 … or international',
        'planning_focus': 'e.g. Golf-first with one safari day',
        'notes': 'Internal CRM notes',
    }
    fieldsets = (
        (
            'Guest',
            {
                'description': (
                    'Primary CRM contact. Assign an owner and keep inquiry_status '
                    'current as the conversation progresses.'
                ),
                'fields': (
                    'full_name',
                    'email',
                    'phone',
                    'preferred_language',
                    'preferred_contact',
                    'inquiry_status',
                    'assigned_to',
                ),
            },
        ),
        (
            'Trip profile',
            {
                'fields': (
                    'budget_band',
                    'trip_flexibility',
                    'planning_focus',
                    'travel_pace',
                    'accommodation_style',
                    'notes',
                ),
            },
        ),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(Inquiry)
class InquiryAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        'lead',
        'inquiry_type',
        'status',
        'target_start_date',
        'guest_count',
        'accommodation_tier',
        'preferred_consultation_date',
        'preferred_consultation_window',
        'created_at',
    )
    list_filter = (
        'inquiry_type',
        'status',
        'accommodation_tier',
        'preferred_consultation_window',
        'target_start_date',
        'created_at',
    )
    list_editable = ('status',)
    search_fields = (
        'lead__full_name',
        'lead__email',
        'lead__phone',
        'additional_requirements',
    )
    autocomplete_fields = ('lead',)
    save_on_top = True
    inlines = [
        InquiryPackageInline,
        InquiryInterestInline,
        InquiryCustomDayInline,
        ConsultationInline,
    ]
    field_placeholders = {
        'additional_requirements': 'Guest free-text notes from the intake form',
    }
    fieldsets = (
        (
            'Inquiry',
            {
                'description': (
                    'One lead can have multiple inquiries. Manage packages, '
                    'shortlist items, planner days, and consultations below.'
                ),
                'fields': (
                    'lead',
                    'inquiry_type',
                    'status',
                    'guest_count',
                    'target_start_date',
                    'accommodation_tier',
                    'preferred_consultation_date',
                    'preferred_consultation_window',
                    'additional_requirements',
                ),
            },
        ),
    )


@admin.register(InquiryInterest)
class InquiryInterestAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'interest_type', 'title_snapshot', 'created_at')
    list_filter = ('interest_type', 'created_at')
    search_fields = ('title_snapshot', 'notes', 'inquiry__lead__email')
    autocomplete_fields = ('inquiry',)


@admin.register(ExperienceInquiry)
class ExperienceInquiryAdmin(
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        'full_name',
        'email',
        'status',
        'context_label',
        'page_url',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = (
        'full_name',
        'email',
        'message',
        'additional_requirements',
        'page_url',
        'context_label',
    )
    readonly_fields = ('created_at', 'page_url', 'context_label')
    actions = ['mark_reviewed', 'mark_closed']
    save_on_top = True
    fieldsets = (
        (
            'Quick enquiry',
            {
                'description': (
                    'Lightweight modal / page enquiries (not a full shortlist). '
                    'Use status actions to mark reviewed or closed.'
                ),
                'fields': (
                    'full_name',
                    'email',
                    'message',
                    'additional_requirements',
                    'status',
                    'context_label',
                    'page_url',
                    'created_at',
                ),
            },
        ),
    )

    @admin.action(description='Mark selected as reviewed')
    def mark_reviewed(self, request, queryset):
        queryset.update(status=ExperienceInquiry.Status.REVIEWED)

    @admin.action(description='Mark selected as closed')
    def mark_closed(self, request, queryset):
        queryset.update(status=ExperienceInquiry.Status.CLOSED)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'scheduled_time', 'status', 'meeting_url')
    list_filter = ('status', 'scheduled_time')
    list_editable = ('status',)
    search_fields = (
        'inquiry__lead__email',
        'inquiry__lead__full_name',
        'meeting_url',
    )
    autocomplete_fields = ('inquiry',)
    fieldsets = (
        (
            None,
            {
                'description': (
                    'Leave meeting_url blank until a call is confirmed — '
                    'confirmation emails should not invent fake Meet links.'
                ),
                'fields': ('inquiry', 'scheduled_time', 'status', 'meeting_url'),
            },
        ),
    )
