from analytics.models import EngagementEvent
from analytics.services import track


BOT_UA_MARKERS = (
    'bot',
    'spider',
    'crawl',
    'slurp',
    'facebookexternalhit',
    'preview',
    'wget',
    'curl',
    'python-requests',
)


class TrackPageViewMixin:
    """
    Record a page-view engagement event after a successful DetailView GET.

    Subclasses set:
      analytics_event_type  – EngagementEvent.EventType value
      analytics_object_type – EngagementEvent.ObjectType value
    """

    analytics_event_type = EngagementEvent.EventType.DESTINATION_VIEW
    analytics_object_type = ''

    def get_analytics_object_id(self):
        obj = getattr(self, 'object', None)
        if obj is None:
            return ''
        slug = getattr(obj, 'slug', None)
        if slug:
            return str(slug)
        return str(getattr(obj, 'pk', '') or '')

    def get_analytics_object_label(self):
        obj = getattr(self, 'object', None)
        if obj is None:
            return ''
        for attr in ('title_en', 'name', 'name_en', 'title', 'slug'):
            value = getattr(obj, attr, None)
            if value:
                return str(value)
        return str(obj)

    def get_analytics_metadata(self):
        obj = getattr(self, 'object', None)
        metadata = {}
        if obj is not None and getattr(obj, 'slug', None):
            metadata['slug'] = obj.slug
        return metadata

    def should_track_analytics(self, request):
        ua = (request.META.get('HTTP_USER_AGENT') or '').lower()
        if not ua:
            return True
        return not any(marker in ua for marker in BOT_UA_MARKERS)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if (
            getattr(response, 'status_code', 500) == 200
            and getattr(self, 'object', None)
            and self.should_track_analytics(request)
        ):
            track(
                event_type=self.analytics_event_type,
                object_type=self.analytics_object_type,
                object_id=self.get_analytics_object_id(),
                object_label=self.get_analytics_object_label(),
                metadata=self.get_analytics_metadata(),
                request=request,
            )
        return response
