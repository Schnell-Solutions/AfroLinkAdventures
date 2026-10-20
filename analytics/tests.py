import json

from django.test import RequestFactory, TestCase, override_settings

from analytics.models import EngagementEvent
from analytics.reporting import counts_by_event_type
from analytics.services import track, track_many
from analytics.views import collect


class EngagementTrackServiceTests(TestCase):
    def test_track_persists_allowed_event(self):
        event = track(
            event_type=EngagementEvent.EventType.PACKAGE_CLICK,
            object_type=EngagementEvent.ObjectType.PACKAGE,
            object_id='kenya-grand-golf-circuit',
            object_label='Kenya Grand Golf Circuit',
            path='/journeys/kenya-grand-golf-circuit/',
            metadata={'slug': 'kenya-grand-golf-circuit'},
        )

        self.assertIsNotNone(event)
        self.assertEqual(EngagementEvent.objects.count(), 1)
        self.assertEqual(event.event_type, EngagementEvent.EventType.PACKAGE_CLICK)

    def test_track_rejects_unknown_event_type(self):
        self.assertIsNone(track(event_type='not_a_real_event'))
        self.assertEqual(EngagementEvent.objects.count(), 0)

    def test_track_many_caps_batch_size(self):
        payloads = [
            {
                'event_type': EngagementEvent.EventType.EVENT_CLICK,
                'object_type': EngagementEvent.ObjectType.EVENT,
                'object_id': str(index),
            }
            for index in range(25)
        ]
        recorded = track_many(payloads)
        self.assertEqual(recorded, 20)
        self.assertEqual(EngagementEvent.objects.count(), 20)

    def test_reporting_counts_by_type(self):
        track(event_type=EngagementEvent.EventType.BANNER_CLICK)
        track(event_type=EngagementEvent.EventType.BANNER_CLICK)
        track(event_type=EngagementEvent.EventType.SEARCH_QUERY)

        counts = counts_by_event_type()
        self.assertEqual(counts[EngagementEvent.EventType.BANNER_CLICK], 2)
        self.assertEqual(counts[EngagementEvent.EventType.SEARCH_QUERY], 1)


@override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'])
class CollectBeaconViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_collect_records_json_batch_from_same_origin(self):
        request = self.factory.post(
            '/analytics/collect/',
            data=json.dumps(
                {
                    'events': [
                        {
                            'event_type': EngagementEvent.EventType.BANNER_CLICK,
                            'object_type': EngagementEvent.ObjectType.BANNER,
                            'object_id': '12',
                        }
                    ]
                }
            ),
            content_type='application/json',
            HTTP_ORIGIN='http://testserver',
            HTTP_HOST='testserver',
        )
        response = collect(request)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EngagementEvent.objects.count(), 1)

    def test_collect_rejects_foreign_origin(self):
        request = self.factory.post(
            '/analytics/collect/',
            data=json.dumps(
                {
                    'event_type': EngagementEvent.EventType.BANNER_CLICK,
                }
            ),
            content_type='application/json',
            HTTP_ORIGIN='https://evil.example',
            HTTP_HOST='testserver',
        )
        response = collect(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(EngagementEvent.objects.count(), 0)
