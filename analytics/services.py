import logging
from typing import Any

from .models import EngagementEvent

logger = logging.getLogger(__name__)

ALLOWED_EVENT_TYPES = {choice.value for choice in EngagementEvent.EventType}
ALLOWED_OBJECT_TYPES = {choice.value for choice in EngagementEvent.ObjectType}

MAX_METADATA_KEYS = 20
MAX_METADATA_VALUE_LENGTH = 500
MAX_PATH_LENGTH = 500
MAX_LABEL_LENGTH = 255
MAX_OBJECT_ID_LENGTH = 64


def _truncate(value: Any, limit: int) -> str:
    text = '' if value is None else str(value)
    return text[:limit]


def _sanitize_metadata(metadata: Any) -> dict:
    if not isinstance(metadata, dict):
        return {}

    cleaned = {}
    for index, (key, value) in enumerate(metadata.items()):
        if index >= MAX_METADATA_KEYS:
            break
        key_text = _truncate(key, 64)
        if isinstance(value, (dict, list)):
            continue
        if value is None:
            cleaned[key_text] = None
        elif isinstance(value, bool):
            cleaned[key_text] = value
        elif isinstance(value, (int, float)):
            cleaned[key_text] = value
        else:
            cleaned[key_text] = _truncate(value, MAX_METADATA_VALUE_LENGTH)
    return cleaned


def request_context(request) -> dict[str, str]:
    if request is None:
        return {'path': '', 'language_code': '', 'session_key': ''}

    session_key = ''
    session = getattr(request, 'session', None)
    if session is not None:
        session_key = getattr(session, 'session_key', None) or ''

    return {
        'path': _truncate(getattr(request, 'path', ''), MAX_PATH_LENGTH),
        'language_code': _truncate(
            getattr(request, 'LANGUAGE_CODE', '') or '',
            8,
        ),
        'session_key': _truncate(session_key, 40),
    }


def track(
    *,
    event_type: str,
    object_type: str = '',
    object_id: str | int | None = '',
    object_label: str = '',
    path: str = '',
    language_code: str = '',
    session_key: str = '',
    metadata: dict | None = None,
    request=None,
) -> EngagementEvent | None:
    """
    Persist one engagement event.

    Failures are logged and swallowed so analytics never affects UX.
    """
    if event_type not in ALLOWED_EVENT_TYPES:
        return None

    if object_type and object_type not in ALLOWED_OBJECT_TYPES:
        object_type = ''

    context = request_context(request) if request is not None else {
        'path': path,
        'language_code': language_code,
        'session_key': session_key,
    }

    try:
        return EngagementEvent.objects.create(
            event_type=event_type,
            object_type=object_type or '',
            object_id=_truncate(object_id or '', MAX_OBJECT_ID_LENGTH),
            object_label=_truncate(object_label or '', MAX_LABEL_LENGTH),
            path=_truncate(path or context['path'], MAX_PATH_LENGTH),
            language_code=_truncate(
                language_code or context['language_code'],
                8,
            ),
            session_key=_truncate(
                session_key or context['session_key'],
                40,
            ),
            metadata=_sanitize_metadata(metadata or {}),
        )
    except Exception:  # noqa: BLE001 - analytics must never break request UX
        logger.exception('Failed to record engagement event %s', event_type)
        return None


def track_many(events: list[dict], request=None) -> int:
    """Insert a small batch of client beacon events. Returns success count."""
    recorded = 0
    for payload in events[:20]:
        if not isinstance(payload, dict):
            continue
        result = track(
            event_type=payload.get('event_type', ''),
            object_type=payload.get('object_type', ''),
            object_id=payload.get('object_id', ''),
            object_label=payload.get('object_label', ''),
            path=payload.get('path', ''),
            metadata=payload.get('metadata'),
            request=request,
        )
        if result is not None:
            recorded += 1
    return recorded
