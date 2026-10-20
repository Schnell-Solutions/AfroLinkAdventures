"""Helpers for inquiry confirmation tokens and consultation windows."""

from __future__ import annotations

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils import timezone

CONFIRMATION_SALT = 'afrolink.inquiry.confirmation'
CONFIRMATION_MAX_AGE = 60 * 60 * 24 * 30  # 30 days
EAT = ZoneInfo('Africa/Nairobi')

WINDOW_START_HOURS = {
    'morning': 9,
    'afternoon': 12,
    'evening': 17,
}


def sign_inquiry_confirmation(inquiry_id: int) -> str:
    return TimestampSigner(salt=CONFIRMATION_SALT).sign(str(inquiry_id))


def unsign_inquiry_confirmation(token: str) -> int:
    raw = TimestampSigner(salt=CONFIRMATION_SALT).unsign(
        token,
        max_age=CONFIRMATION_MAX_AGE,
    )
    return int(raw)


def preferred_window_to_datetime(preferred_date, window_key: str):
    """Map a preferred date + soft window to an EAT datetime for storage."""
    hour = WINDOW_START_HOURS.get(window_key, 12)
    naive = datetime.combine(preferred_date, time(hour=hour, minute=0))
    return timezone.make_aware(naive, EAT)


def earliest_allowed_consultation_date():
    """Tomorrow in EAT — no same-day / past consultation preferences."""
    now_eat = timezone.now().astimezone(EAT)
    return (now_eat + timedelta(days=1)).date()
