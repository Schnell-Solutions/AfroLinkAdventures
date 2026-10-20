"""CSS / URL helpers for safe inline presentation values."""

from __future__ import annotations

from urllib.parse import urlparse


def css_background_image_url(url: str | None) -> str:
    """
    Return a CSS url("...") value safe for inline styles, or ''.

    Rejects non-http(s) schemes and escapes characters that can break out of
    url("...") / url('...') contexts.
    """
    if not url:
        return ''

    raw = str(url).strip()
    if not raw:
        return ''

    try:
        parsed = urlparse(raw)
    except ValueError:
        return ''

    if parsed.scheme not in {'http', 'https'}:
        return ''
    if not parsed.netloc:
        return ''

    # Neutralize characters that terminate CSS url()/string tokens.
    sanitized = (
        raw.replace('\\', '')
        .replace('"', '%22')
        .replace("'", '%27')
        .replace('(', '%28')
        .replace(')', '%29')
        .replace('<', '%3C')
        .replace('>', '%3E')
    )
    return f'url("{sanitized}")'
