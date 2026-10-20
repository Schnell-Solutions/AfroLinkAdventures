"""Parse and validate YouTube watch / short / embed URLs."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

# 11-character YouTube video IDs.
VIDEO_ID_RE = re.compile(r'^[A-Za-z0-9_-]{11}$')

YOUTUBE_HOSTS = {
    'youtube.com',
    'www.youtube.com',
    'm.youtube.com',
    'music.youtube.com',
    'youtu.be',
    'www.youtu.be',
    'youtube-nocookie.com',
    'www.youtube-nocookie.com',
}


def extract_youtube_video_id(url: str | None) -> str | None:
    """
    Return an 11-character YouTube video ID, or None if the URL is blank/invalid.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/live/VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    """
    if not url:
        return None

    raw = str(url).strip()
    if not raw:
        return None

    if '://' not in raw:
        raw = f'https://{raw}'

    try:
        parsed = urlparse(raw)
    except ValueError:
        return None

    host = (parsed.hostname or '').lower()
    if host not in YOUTUBE_HOSTS:
        return None

    path = (parsed.path or '').rstrip('/')
    segments = [segment for segment in path.split('/') if segment]

    candidates: list[str] = []

    if host in {'youtu.be', 'www.youtu.be'} and segments:
        candidates.append(segments[0])
    elif segments:
        if segments[0] in {'embed', 'shorts', 'live', 'v'} and len(segments) >= 2:
            candidates.append(segments[1])
        elif segments[0] == 'watch':
            pass
        elif len(segments) == 1 and VIDEO_ID_RE.fullmatch(segments[0]):
            candidates.append(segments[0])

    query = parse_qs(parsed.query or '')
    for key in ('v', 'vi'):
        if key in query and query[key]:
            candidates.append(query[key][0])

    for candidate in candidates:
        video_id = candidate.split('?')[0].split('&')[0]
        if VIDEO_ID_RE.fullmatch(video_id):
            return video_id

    return None


def youtube_embed_url(url: str | None) -> str | None:
    video_id = extract_youtube_video_id(url)
    if not video_id:
        return None
    return f'https://www.youtube-nocookie.com/embed/{video_id}'
