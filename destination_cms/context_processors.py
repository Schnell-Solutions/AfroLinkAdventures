from .models import PromotionalBanner, Region
from .promotions import package_promotion_banner_slides


def navigation_regions(request):
    regions = list(
        Region.objects.filter(is_active=True).only(
            'name_en',
            'name_de',
            'slug',
            'country_en',
            'country_de',
        ).order_by('name_en')
    )

    language_code = getattr(request, 'LANGUAGE_CODE', 'en') or 'en'
    country_groups = []
    groups_by_country = {}

    for region in regions:
        country_name = region.get_country_name(language_code)
        if not country_name:
            country_name = 'Other'
        if country_name not in groups_by_country:
            groups_by_country[country_name] = {
                'country': country_name,
                'regions': [],
            }
            country_groups.append(groups_by_country[country_name])
        groups_by_country[country_name]['regions'].append(region)

    return {
        'nav_regions': regions,
        'nav_region_groups': country_groups,
        'nav_region_grouped': len(country_groups) > 1,
    }


def active_promotional_banners(request):
    # Skip admin and other non-public surfaces to avoid wasted queries.
    path = getattr(request, 'path', '') or ''
    if path.startswith('/admin/') or path.startswith('/analytics/'):
        return {
            'promotional_banners': [],
            'has_promotional_banners': False,
        }

    language_code = getattr(request, 'LANGUAGE_CODE', 'en') or 'en'
    # Package-linked promos first so CTAs resolve to a specific journey detail,
    # ahead of any broader CMS banners that may point at listing pages.
    banners = list(package_promotion_banner_slides(language_code=language_code))
    banners.extend(list(PromotionalBanner.active_queryset()))
    return {
        'promotional_banners': banners,
        'has_promotional_banners': bool(banners),
    }

