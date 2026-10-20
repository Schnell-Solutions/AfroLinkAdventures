from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from destination_cms.models import BasePackage, PackagePricingSeason, PackagePromotion
from destination_cms.promotions import featured_special_offer_cards


ORIGINAL_SLUGS = frozenset(
    {
        'executive-equator-wilderness-challenge',
        'kenya-grand-golf-circuit',
        'nairobi-championship-golf-week',
        'ultimate-odyssey',
    }
)


class Command(BaseCommand):
    help = (
        'Remove promos from the original four packages and seed three promo '
        'test packages (one per journey focus).'
    )

    def handle(self, *args, **options):
        deleted, _ = PackagePromotion.objects.filter(
            package__slug__in=ORIGINAL_SLUGS
        ).delete()
        self.stdout.write(f'Removed {deleted} promo row(s) from original packages.')

        BasePackage.objects.filter(
            slug='executive-equator-wilderness-challenge'
        ).update(package_type=BasePackage.PackageType.GOLF_SAFARI)
        BasePackage.objects.filter(
            slug__in=ORIGINAL_SLUGS - {'executive-equator-wilderness-challenge'}
        ).update(package_type=BasePackage.PackageType.GOLF)

        media_by_slug = {
            package.slug: (package.card_image_url, package.hero_image_url)
            for package in BasePackage.objects.filter(slug__in=ORIGINAL_SLUGS)
        }
        fallback_card, fallback_hero = next(iter(media_by_slug.values()), ('', ''))

        now = timezone.now()
        start = now - timedelta(days=1)
        end = now + timedelta(days=90)
        season_start = (now - timedelta(days=30)).date()
        season_end = (now + timedelta(days=180)).date()

        specs = [
            {
                'slug': 'promo-amboseli-safari-escape',
                'title_en': '8-Day Amboseli Safari Escape',
                'title_de': '8-Tage Amboseli Safari Escape',
                'summary_en': (
                    'Private game drives beneath Kilimanjaro with bush breakfasts '
                    'and a conservancy night drive. Built for guests who want a '
                    'pure safari rhythm.'
                ),
                'summary_de': (
                    'Private Game Drives unter dem Kilimandscharo mit Bush Breakfast '
                    'und Conservancy Night Drive.'
                ),
                'package_type': BasePackage.PackageType.SAFARI,
                'duration_days': 8,
                'price': Decimal('8750'),
                'price_high': Decimal('10250'),
                'media_from': 'executive-equator-wilderness-challenge',
                'promo': {
                    'label': 'Amboseli Early Booking',
                    'discount_type': PackagePromotion.DiscountType.PERCENTAGE,
                    'discount_value': Decimal('12'),
                    'show_featured_badge': True,
                    'show_in_banner': True,
                    'banner_title': 'Amboseli Safari Escape — 12% Off',
                    'banner_description': (
                        'Limited early booking saving on our 8-day Amboseli safari.'
                    ),
                    'banner_cta_text': 'View Safari Offer',
                    'display_order': 10,
                },
            },
            {
                'slug': 'promo-nakuru-fairways-retreat',
                'title_en': '6-Day Nakuru Fairways Retreat',
                'title_de': '6-Tage Nakuru Fairways Retreat',
                'summary_en': (
                    'Championship golf around Lake Nakuru with clubhouse hosting '
                    'and a relaxed highland pace. Ideal for golf-first travellers.'
                ),
                'summary_de': (
                    'Championship-Golf rund um den Lake Nakuru mit Clubhaus-Service '
                    'und entspanntem Highland-Tempo.'
                ),
                'package_type': BasePackage.PackageType.GOLF,
                'duration_days': 6,
                'price': Decimal('5950'),
                'price_high': Decimal('6850'),
                'media_from': 'nairobi-championship-golf-week',
                'promo': {
                    'label': 'Fairways Midweek Promo',
                    'discount_type': PackagePromotion.DiscountType.FIXED,
                    'discount_value': Decimal('650'),
                    'show_featured_badge': True,
                    'show_in_banner': False,
                    'banner_title': '',
                    'banner_description': '',
                    'banner_cta_text': '',
                    'display_order': 20,
                },
            },
            {
                'slug': 'promo-masaai-mara-golf-safari',
                'title_en': '10-Day Mara Golf & Safari Balance',
                'title_de': '10-Tage Mara Golf & Safari Balance',
                'summary_en': (
                    'Morning tee times paired with afternoon game drives in the Mara '
                    '— a balanced golf and safari itinerary for couples and small groups.'
                ),
                'summary_de': (
                    'Vormittag auf dem Fairway, Nachmittag auf Safari in der Mara — '
                    'ausgewogen fuer Paare und kleine Gruppen.'
                ),
                'package_type': BasePackage.PackageType.GOLF_SAFARI,
                'duration_days': 10,
                'price': Decimal('11850'),
                'price_high': Decimal('13950'),
                'media_from': 'kenya-grand-golf-circuit',
                'promo': {
                    'label': 'Mara Balance Offer',
                    'discount_type': PackagePromotion.DiscountType.PERCENTAGE,
                    'discount_value': Decimal('10'),
                    'show_featured_badge': False,
                    'show_in_banner': True,
                    'banner_title': 'Mara Golf & Safari — 10% Off',
                    'banner_description': (
                        'A balanced golf and safari week with a seasonal saving.'
                    ),
                    'banner_cta_text': 'View Combined Offer',
                    'display_order': 30,
                },
            },
        ]

        for spec in specs:
            card_url, hero_url = media_by_slug.get(
                spec['media_from'],
                (fallback_card, fallback_hero),
            )
            package, created = BasePackage.objects.update_or_create(
                slug=spec['slug'],
                defaults={
                    'title_en': spec['title_en'],
                    'title_de': spec['title_de'],
                    'summary_en': spec['summary_en'],
                    'summary_de': spec['summary_de'],
                    'package_type': spec['package_type'],
                    'duration_days': spec['duration_days'],
                    'card_image_url': card_url or '',
                    'hero_image_url': hero_url or '',
                    'is_active': True,
                    'inclusions_en': (
                        'Private guiding\nSelected lodge nights\n'
                        'Park fees\nDaily breakfast'
                    ),
                    'exclusions_en': (
                        'International flights\nVisa fees\nPersonal expenses'
                    ),
                },
            )
            PackagePricingSeason.objects.filter(base_package=package).delete()
            PackagePricingSeason.objects.create(
                base_package=package,
                season_name='Green Season',
                start_date=season_start,
                end_date=season_end,
                price_usd=spec['price'],
            )
            PackagePricingSeason.objects.create(
                base_package=package,
                season_name='Peak Season',
                start_date=season_end + timedelta(days=1),
                end_date=season_end + timedelta(days=120),
                price_usd=spec['price_high'],
            )
            promo_spec = spec['promo']
            PackagePromotion.objects.update_or_create(
                package=package,
                label=promo_spec['label'],
                defaults={
                    'discount_type': promo_spec['discount_type'],
                    'discount_value': promo_spec['discount_value'],
                    'show_featured_badge': promo_spec['show_featured_badge'],
                    'show_in_banner': promo_spec['show_in_banner'],
                    'banner_title': promo_spec['banner_title'],
                    'banner_description': promo_spec['banner_description'],
                    'banner_cta_text': promo_spec['banner_cta_text'],
                    'is_active': True,
                    'start_date': start,
                    'end_date': end,
                    'display_order': promo_spec['display_order'],
                },
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} {package.slug} ({package.package_type})')

        cards = featured_special_offer_cards(limit=3)
        self.stdout.write(f'Special Offers cards: {len(cards)}')
        for card in cards:
            self.stdout.write(
                f"  - {card['package'].slug} | {card['package_type_label']} | "
                f"featured={card['is_featured_promo']} | "
                f"{card['promo_price_label']} / {card['original_price_label']}"
            )
