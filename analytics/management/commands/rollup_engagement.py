from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from analytics.models import EngagementDailyRollup, EngagementEvent


class Command(BaseCommand):
    help = (
        'Rebuild EngagementDailyRollup rows for dashboard charts. '
        'Safe to re-run; upserts by (day, event_type, object_type, object_id).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='How many recent days to roll up (default: 90).',
        )

    def handle(self, *args, **options):
        days = max(1, options['days'])
        since = timezone.now() - timedelta(days=days)

        rows = (
            EngagementEvent.objects.filter(created_at__gte=since)
            .annotate(day=TruncDate('created_at'))
            .values('day', 'event_type', 'object_type', 'object_id')
            .annotate(total=Count('id'))
        )

        upserted = 0
        for row in rows:
            _, created = EngagementDailyRollup.objects.update_or_create(
                day=row['day'],
                event_type=row['event_type'],
                object_type=row['object_type'] or '',
                object_id=row['object_id'] or '',
                defaults={'count': row['total']},
            )
            upserted += 1

        self.stdout.write(
            self.style.SUCCESS(f'Upserted {upserted} daily rollup row(s).')
        )
