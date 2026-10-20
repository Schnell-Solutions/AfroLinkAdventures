from decimal import Decimal, ROUND_HALF_UP
from types import SimpleNamespace

from django.db.models import Prefetch
from django.urls import reverse
from django.utils.translation import gettext as _


def money_int(value):
    return int(Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def format_usd(amount):
    if amount is None:
        return None
    return f'${int(amount):,}'


def package_starting_price(base_package):
    prices = [
        season.price_usd
        for season in base_package.pricing_seasons.all()
    ]
    return min(prices) if prices else None


def get_active_promotion_for_package(base_package, at=None):
    """Return the highest-priority active promotion already loaded or queried."""
    active = getattr(base_package, 'active_promotions', None)
    if active is not None:
        return active[0] if active else None

    from .models import PackagePromotion

    return (
        PackagePromotion.active_queryset(at=at)
        .filter(package_id=base_package.pk)
        .first()
    )


def apply_promotion(base_price, promotion):
    if base_price is None or promotion is None:
        return None, None

    from .models import PackagePromotion

    original = money_int(base_price)

    if promotion.discount_type == PackagePromotion.DiscountType.PERCENTAGE:
        factor = Decimal('1') - (Decimal(promotion.discount_value) / Decimal('100'))
        discounted = money_int(Decimal(original) * factor)
    else:
        discounted = max(0, original - money_int(promotion.discount_value))

    savings = max(0, original - discounted)
    return discounted, savings


def build_package_pricing(base_package, at=None):
    original_price = package_starting_price(base_package)
    promotion = get_active_promotion_for_package(base_package, at=at)
    promo_price = None
    savings = None

    if original_price is not None and promotion is not None:
        promo_price, savings = apply_promotion(original_price, promotion)

    has_promo_price = (
        promo_price is not None
        and original_price is not None
        and savings is not None
        and savings > 0
    )

    if has_promo_price:
        starting_price_label = _('From %(price)s') % {'price': format_usd(promo_price)}
        original_price_label = _('From %(price)s') % {'price': format_usd(original_price)}
        savings_label = _('Save %(amount)s') % {'amount': format_usd(savings)}
        sort_price = promo_price
    elif original_price is not None:
        starting_price_label = _('From %(price)s') % {'price': format_usd(original_price)}
        original_price_label = starting_price_label
        savings_label = ''
        sort_price = original_price
    else:
        starting_price_label = str(_('Pricing on request'))
        original_price_label = starting_price_label
        savings_label = ''
        sort_price = None

    return {
        'original_price': original_price,
        'promo_price': promo_price if has_promo_price else None,
        'savings': savings if has_promo_price else None,
        'has_promo_price': has_promo_price,
        'starting_price': sort_price if sort_price is not None else original_price,
        'starting_price_label': starting_price_label,
        'original_price_label': original_price_label,
        'promo_price_label': (
            _('From %(price)s') % {'price': format_usd(promo_price)}
            if has_promo_price
            else ''
        ),
        'savings_label': savings_label,
        'promotion': promotion,
        'promo_label': promotion.label if promotion else '',
        'is_featured_promo': bool(promotion and promotion.show_featured_badge),
        'package_type_label': base_package.get_package_type_display(),
    }


def build_package_card(base_package, at=None):
    pricing = build_package_pricing(base_package, at=at)
    return {
        'package': base_package,
        'image_url': base_package.card_image_url or base_package.hero_image_url,
        **pricing,
    }


def active_promotions_prefetch():
    from .models import PackagePromotion

    return Prefetch(
        'promotions',
        queryset=PackagePromotion.active_queryset().select_related('package'),
        to_attr='active_promotions',
    )


def featured_special_offer_cards(limit=3):
    """Homepage Special Offers: featured+discounted first, then other discounts."""
    from .models import PackagePromotion

    promotions = list(
        PackagePromotion.active_queryset()
        .filter(package__is_active=True)
        .select_related('package')
        .prefetch_related('package__pricing_seasons')
    )

    featured = [p for p in promotions if p.show_featured_badge]
    fillers = [p for p in promotions if not p.show_featured_badge]
    ordered = featured + fillers

    cards = []
    seen_packages = set()
    for promotion in ordered:
        if promotion.package_id in seen_packages:
            continue
        package = promotion.package
        package.active_promotions = [promotion]
        card = build_package_card(package)
        if not card['has_promo_price']:
            continue
        seen_packages.add(promotion.package_id)
        cards.append(card)
        if len(cards) >= limit:
            break
    return cards


def package_promotion_banner_slides(language_code='en'):
    """Adapt package promotions flagged for the top banner."""
    from .models import PackagePromotion

    slides = []
    promotions = (
        PackagePromotion.active_queryset()
        .filter(show_in_banner=True, package__is_active=True)
        .select_related('package')
        .prefetch_related('package__pricing_seasons')
    )
    use_de = (language_code or 'en').startswith('de')
    for promotion in promotions:
        package = promotion.package
        package.active_promotions = [promotion]
        pricing = build_package_pricing(package)
        description = (promotion.banner_description or '').strip()
        if not description:
            parts = [promotion.label]
            if pricing['savings_label']:
                parts.append(pricing['savings_label'])
            description = ' · '.join(parts)[:280]

        package_title = (
            package.title_de
            if use_de and package.title_de
            else package.title_en
        )
        title = (promotion.banner_title or '').strip() or package_title
        cta_text = (promotion.banner_cta_text or '').strip() or str(_('View Offer'))
        type_label = promotion.label or str(_('Special Offer'))

        slide = SimpleNamespace(
            id=f'package-promo-{promotion.id}',
            title=title[:160],
            short_description=description[:280],
            cta_text=cta_text[:80],
            cta_url=reverse(
                'destination_cms:package_detail',
                kwargs={'slug': package.slug},
            ),
            background_image_url=(
                package.hero_image_url or package.card_image_url or ''
            ),
            promotion_type_display=type_label,
            is_dismissible=True,
        )
        slide.get_promotion_type_display = lambda label=type_label: label
        slides.append(slide)
    return slides
