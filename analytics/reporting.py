"""
Query helpers for a future analytics dashboard.

Prefer EngagementDailyRollup for chart ranges; fall back to EngagementEvent
for ad-hoc drill-downs.
"""

from datetime import date, timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import EngagementDailyRollup, EngagementEvent


def counts_by_event_type(*, since=None, until=None):
    queryset = EngagementEvent.objects.all()
    if since is not None:
        queryset = queryset.filter(created_at__gte=since)
    if until is not None:
        queryset = queryset.filter(created_at__lt=until)
    return {
        row['event_type']: row['total']
        for row in queryset.values('event_type').annotate(total=Count('id'))
    }


def top_objects(*, event_type, limit=10, since=None, until=None):
    queryset = EngagementEvent.objects.filter(event_type=event_type).exclude(
        object_id='',
    )
    if since is not None:
        queryset = queryset.filter(created_at__gte=since)
    if until is not None:
        queryset = queryset.filter(created_at__lt=until)
    return list(
        queryset.values('object_type', 'object_id', 'object_label')
        .annotate(total=Count('id'))
        .order_by('-total')[:limit]
    )


def daily_series(*, event_type=None, days=30):
    """Return daily counts from rollups when present, else raw events."""
    end = timezone.localdate()
    start = end - timedelta(days=max(days - 1, 0))

    rollup = EngagementDailyRollup.objects.filter(day__gte=start, day__lte=end)
    if event_type:
        rollup = rollup.filter(event_type=event_type)

    if rollup.exists():
        rows = (
            rollup.values('day')
            .annotate(total=Sum('count'))
            .order_by('day')
        )
        return [{'day': row['day'], 'total': row['total'] or 0} for row in rows]

    queryset = EngagementEvent.objects.filter(
        created_at__date__gte=start,
        created_at__date__lte=end,
    )
    if event_type:
        queryset = queryset.filter(event_type=event_type)

    rows = (
        queryset.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )
    return [{'day': row['day'], 'total': row['total']} for row in rows]


def empty_day_range(days=30) -> list[date]:
    end = timezone.localdate()
    start = end - timedelta(days=max(days - 1, 0))
    return [start + timedelta(days=offset) for offset in range((end - start).days + 1)]
