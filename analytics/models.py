from django.db import models


class EngagementEvent(models.Model):
    """Append-only engagement fact for reporting and future dashboards."""

    class EventType(models.TextChoices):
        BANNER_CLICK = 'banner_click', 'Promotion banner click'
        EVENT_CLICK = 'event_click', 'Event click'
        PACKAGE_CLICK = 'package_click', 'Package click'
        PACKAGE_VIEW = 'package_view', 'Package page view'
        EVENT_VIEW = 'event_view', 'Event page view'
        DESTINATION_VIEW = 'destination_view', 'Destination page view'
        JOURNAL_VIEW = 'journal_view', 'Journal page view'
        INQUIRY_SUBMIT = 'inquiry_submit', 'Inquiry submission'
        SEARCH_QUERY = 'search_query', 'Search inquiry'

    class ObjectType(models.TextChoices):
        BANNER = 'banner', 'Promotional banner'
        PACKAGE_PROMO = 'package_promo', 'Package promotion banner'
        PACKAGE = 'package', 'Package / journey'
        EVENT = 'event', 'Golf event'
        REGION = 'region', 'Region'
        COURSE = 'course', 'Golf course'
        SAFARI = 'safari', 'Safari destination'
        ACCOMMODATION = 'accommodation', 'Accommodation'
        WELLNESS = 'wellness', 'Wellness experience'
        JOURNAL = 'journal', 'Journal article'
        INQUIRY = 'inquiry', 'Inquiry'
        EXPERIENCE_INQUIRY = 'experience_inquiry', 'Experience inquiry'
        LISTING = 'listing', 'Listing / search surface'

    event_type = models.CharField(
        max_length=32,
        choices=EventType.choices,
        db_index=True,
    )
    object_type = models.CharField(
        max_length=32,
        choices=ObjectType.choices,
        blank=True,
        default='',
        db_index=True,
    )
    object_id = models.CharField(
        max_length=64,
        blank=True,
        default='',
        db_index=True,
        help_text='Stable identifier (primary key or slug).',
    )
    object_label = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='Denormalized label for reporting without joins.',
    )
    path = models.CharField(max_length=500, blank=True, default='')
    language_code = models.CharField(max_length=8, blank=True, default='')
    session_key = models.CharField(max_length=40, blank=True, default='', db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['object_type', 'object_id', 'created_at']),
            models.Index(fields=['event_type', 'object_type', 'created_at']),
        ]

    def __str__(self):
        target = self.object_label or self.object_id or self.path or '—'
        return f'{self.get_event_type_display()} · {target}'


class EngagementDailyRollup(models.Model):
    """
    Pre-aggregated daily counters for dashboard charts.

    Populated by `python manage.py rollup_engagement` (not on every write)
    so ingest stays a single cheap INSERT.
    """

    day = models.DateField(db_index=True)
    event_type = models.CharField(
        max_length=32,
        choices=EngagementEvent.EventType.choices,
        db_index=True,
    )
    object_type = models.CharField(max_length=32, blank=True, default='')
    object_id = models.CharField(max_length=64, blank=True, default='')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-day', 'event_type']
        constraints = [
            models.UniqueConstraint(
                fields=['day', 'event_type', 'object_type', 'object_id'],
                name='analytics_daily_rollup_uniq',
            ),
        ]
        indexes = [
            models.Index(fields=['day', 'event_type']),
        ]

    def __str__(self):
        return f'{self.day} · {self.event_type} · {self.count}'
