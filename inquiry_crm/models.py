from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from destination_cms.models import BasePackage, GolfCourse, Region, SafariDestination


class Lead(models.Model):
    class PreferredLanguage(models.TextChoices):
        ENGLISH = 'en', 'English'
        GERMAN = 'de', 'German'

    class InquiryStatus(models.TextChoices):
        NEW = 'New', 'New'
        CONSULTATION = 'Consultation', 'Consultation'
        PROPOSAL_SENT = 'Proposal Sent', 'Proposal Sent'
        CLOSED_WON = 'Closed Won', 'Closed Won'

    class BudgetBand(models.TextChoices):
        UNDER_15K = 'under_15k', 'Under $15,000'
        BAND_15_30K = '15_30k', '$15,000 – $30,000'
        BAND_30_50K = '30_50k', '$30,000 – $50,000'
        OVER_50K = 'over_50k', '$50,000+'
        OPEN = 'open', 'Open / discuss on the call'

    class TripFlexibility(models.TextChoices):
        FIXED = 'fixed', 'Fixed dates'
        FEW_DAYS = 'few_days', 'Flexible by a few days'
        MONTH = 'month', 'Flexible within the month'
        FULLY = 'fully', 'Fully flexible'

    class PreferredContact(models.TextChoices):
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone'
        WHATSAPP = 'whatsapp', 'WhatsApp'

    full_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=40, blank=True, db_index=True)
    preferred_language = models.CharField(
        max_length=2,
        choices=PreferredLanguage.choices,
        default=PreferredLanguage.ENGLISH,
        db_index=True,
    )
    preferred_contact = models.CharField(
        max_length=20,
        choices=PreferredContact.choices,
        default=PreferredContact.EMAIL,
        db_index=True,
    )
    budget_band = models.CharField(
        max_length=20,
        choices=BudgetBand.choices,
        blank=True,
        db_index=True,
    )
    trip_flexibility = models.CharField(
        max_length=20,
        choices=TripFlexibility.choices,
        blank=True,
        db_index=True,
    )
    inquiry_status = models.CharField(
        max_length=50,
        choices=InquiryStatus.choices,
        default=InquiryStatus.NEW,
        db_index=True,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_leads',
        blank=True,
        null=True,
        db_index=True,
        help_text='Staff member currently owning follow-up.',
    )
    planning_focus = models.CharField(max_length=120, blank=True)
    travel_pace = models.CharField(max_length=120, blank=True)
    accommodation_style = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} <{self.email}>'


class Inquiry(models.Model):
    class InquiryType(models.TextChoices):
        PRE_SET_PACKAGES = 'pre_set_packages', 'Pre-set Packages'
        CUSTOM_BUILD = 'custom_build', 'Custom Build'
        MIXED = 'mixed', 'Mixed'

    class AccommodationTier(models.TextChoices):
        STANDARD_LUXURY = 'standard_luxury', 'Standard Luxury'
        PREMIUM_CHARTER = 'premium_charter', 'Premium Charter'

    class PreferredWindow(models.TextChoices):
        MORNING = 'morning', 'Morning (09:00–12:00 EAT)'
        AFTERNOON = 'afternoon', 'Afternoon (12:00–17:00 EAT)'
        EVENING = 'evening', 'Evening (17:00–20:00 EAT)'

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='inquiries',
        db_index=True,
    )
    inquiry_type = models.CharField(
        max_length=50,
        choices=InquiryType.choices,
        db_index=True,
    )
    status = models.CharField(
        max_length=50,
        choices=Lead.InquiryStatus.choices,
        default=Lead.InquiryStatus.NEW,
        db_index=True,
    )
    target_start_date = models.DateField(blank=True, null=True, db_index=True)
    guest_count = models.PositiveSmallIntegerField(default=2)
    accommodation_tier = models.CharField(
        max_length=50,
        choices=AccommodationTier.choices,
        default=AccommodationTier.STANDARD_LUXURY,
        db_index=True,
    )
    preferred_consultation_date = models.DateField(blank=True, null=True)
    preferred_consultation_window = models.CharField(
        max_length=20,
        choices=PreferredWindow.choices,
        blank=True,
    )
    luggage_limit_acknowledged = models.BooleanField(default=False)
    additional_requirements = models.TextField(
        blank=True,
        help_text='Preferences, changes, accessibility, dietary needs, and other considerations.',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.lead} - {self.get_inquiry_type_display()}'


class InquiryPackage(models.Model):
    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name='package_shortlist',
        db_index=True,
    )
    base_package = models.ForeignKey(
        BasePackage,
        on_delete=models.PROTECT,
        related_name='inquiry_shortlists',
        db_index=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['inquiry', 'base_package__title_en']
        constraints = [
            models.UniqueConstraint(
                fields=['inquiry', 'base_package'],
                name='unique_inquiry_package',
            ),
        ]

    def __str__(self):
        return f'{self.inquiry} - {self.base_package}'


class InquiryCustomDay(models.Model):
    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name='custom_days',
        db_index=True,
    )
    day_number = models.PositiveIntegerField(db_index=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='inquiry_custom_days',
        db_index=True,
    )
    golf_course = models.ForeignKey(
        GolfCourse,
        on_delete=models.SET_NULL,
        related_name='inquiry_custom_days',
        db_index=True,
        blank=True,
        null=True,
    )
    safari_extension = models.ForeignKey(
        SafariDestination,
        on_delete=models.SET_NULL,
        related_name='inquiry_custom_days',
        db_index=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['inquiry', 'day_number']
        constraints = [
            models.UniqueConstraint(
                fields=['inquiry', 'day_number'],
                name='unique_inquiry_custom_day',
            ),
        ]

    def __str__(self):
        return f'{self.inquiry} - Custom Day {self.day_number}'


class InquiryInterest(models.Model):
    class InterestType(models.TextChoices):
        GOLF_COURSE = 'golf_course', 'Golf Course'
        SAFARI_EXTENSION = 'safari_extension', 'Safari Destination'
        ACCOMMODATION = 'accommodation', 'Accommodation'
        WELLNESS_EXPERIENCE = 'wellness_experience', 'Wellness Experience'
        GOLF_EVENT = 'golf_event', 'Golf Event'

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name='interests',
        db_index=True,
    )
    interest_type = models.CharField(
        max_length=50,
        choices=InterestType.choices,
        db_index=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    title_snapshot = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['inquiry', 'interest_type', 'title_snapshot']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['inquiry', 'content_type', 'object_id'],
                name='unique_inquiry_interest_object',
            ),
        ]

    def __str__(self):
        return f'{self.inquiry} - {self.title_snapshot}'


class Consultation(models.Model):
    class ConsultationStatus(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name='consultations',
        db_index=True,
    )
    scheduled_time = models.DateTimeField(db_index=True)
    meeting_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Filled in by the team once the consultation link is ready.',
    )
    status = models.CharField(
        max_length=20,
        choices=ConsultationStatus.choices,
        default=ConsultationStatus.SCHEDULED,
        db_index=True,
    )

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f'{self.inquiry} consultation at {self.scheduled_time}'


class ExperienceInquiry(models.Model):
    """Lightweight inquiry from empty states when a guest cannot find an experience."""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        REVIEWED = 'reviewed', 'Reviewed'
        CLOSED = 'closed', 'Closed'

    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(db_index=True)
    message = models.TextField(
        help_text='What the guest is looking for (destination, golf, safari, stay, etc.).',
    )
    additional_requirements = models.TextField(
        blank=True,
        help_text='Preferences, changes, accessibility, dietary needs, and other considerations.',
    )
    page_url = models.CharField(max_length=500, blank=True)
    context_label = models.CharField(
        max_length=255,
        blank=True,
        help_text='Prefill context from the page (region, course name, etc.).',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'experience inquiries'

    def __str__(self):
        label = self.full_name or self.email
        return f'{label} — {self.message[:60]}'
