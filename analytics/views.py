import json
from urllib.parse import urlparse

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import track_many

COLLECT_RATE_LIMIT = 60  # events batches per minute per client key
COLLECT_RATE_WINDOW = 60


def _request_hostname(request) -> str:
    host = request.META.get('HTTP_HOST') or request.META.get('SERVER_NAME') or ''
    return host.split(':')[0].lower()


def _host_matches(request, url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if not parsed.netloc:
        return False
    request_host = _request_hostname(request)
    url_host = parsed.netloc.split(':')[0].lower()
    return bool(request_host) and url_host == request_host


def _is_trusted_beacon(request) -> bool:
    """Allow same-origin beacons without CSRF (sendBeacon cannot set headers)."""
    fetch_site = (request.META.get('HTTP_SEC_FETCH_SITE') or '').lower()
    if fetch_site == 'same-origin':
        return True

    origin = request.META.get('HTTP_ORIGIN', '')
    if origin:
        return _host_matches(request, origin)
    referer = request.META.get('HTTP_REFERER', '')
    if referer:
        return _host_matches(request, referer)
    return False


def _client_key(request) -> str:
    session = getattr(request, 'session', None)
    session_key = getattr(session, 'session_key', None) if session else None
    if session_key:
        return f'session:{session_key}'
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return f'ip:{forwarded.split(",")[0].strip()}'
    return f'ip:{request.META.get("REMOTE_ADDR", "unknown")}'


def _rate_limited(request) -> bool:
    key = f'analytics:collect:{_client_key(request)}'
    try:
        current = cache.get(key, 0)
        if current >= COLLECT_RATE_LIMIT:
            return True
        if current:
            cache.incr(key)
        else:
            cache.set(key, 1, timeout=COLLECT_RATE_WINDOW)
    except Exception:  # noqa: BLE001 - never block analytics on cache issues
        return False
    return False


@csrf_exempt
@require_POST
def collect(request):
    """
    Lightweight beacon endpoint for client-side engagement events.

    Accepts JSON: {"events": [{event_type, object_type, object_id, ...}, ...]}
    or a single event object.
    """
    if not _is_trusted_beacon(request):
        return HttpResponseForbidden('origin not allowed')

    if _rate_limited(request):
        return HttpResponse(status=204)

    content_type = (request.META.get('CONTENT_TYPE') or '').split(';')[0].strip()
    raw = request.body or b''

    if len(raw) > 16_384:
        return HttpResponseBadRequest('payload too large')

    payload = None
    if content_type == 'application/json' or raw[:1] in (b'{', b'['):
        try:
            payload = json.loads(raw.decode('utf-8') or '{}')
        except (UnicodeDecodeError, json.JSONDecodeError):
            return HttpResponseBadRequest('invalid json')
    else:
        events_raw = request.POST.get('events')
        if events_raw:
            try:
                payload = {'events': json.loads(events_raw)}
            except json.JSONDecodeError:
                return HttpResponseBadRequest('invalid events')
        else:
            payload = request.POST.dict()

    if isinstance(payload, list):
        events = payload
    elif isinstance(payload, dict):
        if 'events' in payload and isinstance(payload['events'], list):
            events = payload['events']
        elif payload.get('event_type'):
            events = [payload]
        else:
            events = []
    else:
        events = []

    if not events:
        return HttpResponseBadRequest('no events')

    recorded = track_many(events, request=request)

    if 'application/json' in (request.headers.get('Accept') or ''):
        return JsonResponse({'ok': True, 'recorded': recorded})
    return HttpResponse(status=204)
