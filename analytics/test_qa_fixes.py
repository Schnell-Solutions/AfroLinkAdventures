from django.test import RequestFactory, TestCase

from analytics.models import EngagementEvent
from analytics.services import track
from analytics.views import collect
from destination_cms.css_utils import css_background_image_url
from destination_cms.youtube import extract_youtube_video_id


class AnalyticsResilienceTests(TestCase):
    def test_track_swallows_unexpected_errors(self):
        original_create = EngagementEvent.objects.create

        def boom(**kwargs):
            raise RuntimeError('simulated failure')

        EngagementEvent.objects.create = boom
        try:
            self.assertIsNone(
                track(
                    event_type=EngagementEvent.EventType.PACKAGE_CLICK,
                    object_id='x',
                )
            )
        finally:
            EngagementEvent.objects.create = original_create


class CollectBeaconHardeningTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_accepts_sec_fetch_site_same_origin(self):
        request = self.factory.post(
            '/analytics/collect/',
            data='{"event_type":"banner_click","object_id":"1"}',
            content_type='application/json',
            HTTP_SEC_FETCH_SITE='same-origin',
            HTTP_HOST='127.0.0.1:8000',
        )
        response = collect(request)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EngagementEvent.objects.count(), 1)


class PresentationHelperTests(TestCase):
    def test_css_bg_image_rejects_non_http(self):
        self.assertEqual(css_background_image_url('javascript:alert(1)'), '')

    def test_youtube_short_links(self):
        self.assertEqual(
            extract_youtube_video_id('https://youtu.be/dQw4w9WgXcQ'),
            'dQw4w9WgXcQ',
        )
        self.assertIsNone(extract_youtube_video_id('https://vimeo.com/123'))
