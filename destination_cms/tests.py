from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase
from django.utils import timezone

from destination_cms.context_processors import (
    active_promotional_banners,
    navigation_regions,
)
from destination_cms.models import (
    BasePackage,
    PackagePricingSeason,
    PackagePromotion,
    Region,
)
from destination_cms.promotions import (
    apply_promotion,
    build_package_pricing,
    featured_special_offer_cards,
    package_promotion_banner_slides,
)


class NavigationRegionsContextProcessorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_groups_regions_by_country_when_multiple_countries_exist(self):
        kenya_region = Region.objects.create(
            name_en='Nairobi & Environs',
            name_de='Nairobi & Umgebung',
            slug='nairobi-environs',
            country_en='Kenya',
            country_de='Kenia',
        )
        tanzania_region = Region.objects.create(
            name_en='Serengeti Coast',
            name_de='Serengeti Küste',
            slug='serengeti-coast',
            country_en='Tanzania',
            country_de='Tansania',
        )

        request = self.factory.get('/')
        request.LANGUAGE_CODE = 'en'

        context = navigation_regions(request)

        grouped_regions = context['nav_region_groups']

        self.assertEqual([group['country'] for group in grouped_regions], ['Kenya', 'Tanzania'])
        self.assertEqual(grouped_regions[0]['regions'][0].slug, kenya_region.slug)
        self.assertEqual(grouped_regions[1]['regions'][0].slug, tanzania_region.slug)

    def test_uses_flat_region_list_when_all_regions_share_one_country(self):
        kenya_region_one = Region.objects.create(
            name_en='Nairobi & Environs',
            name_de='Nairobi & Umgebung',
            slug='nairobi-environs',
            country_en='Kenya',
            country_de='Kenia',
        )
        kenya_region_two = Region.objects.create(
            name_en='The Coastal Strip',
            name_de='Der Küstenstreifen',
            slug='coastal-strip',
            country_en='Kenya',
            country_de='Kenia',
        )

        request = self.factory.get('/')
        request.LANGUAGE_CODE = 'en'

        context = navigation_regions(request)

        self.assertEqual(context['nav_regions'][0].slug, kenya_region_one.slug)
        self.assertEqual(context['nav_regions'][1].slug, kenya_region_two.slug)
        self.assertEqual(context['nav_region_groups'][0]['country'], 'Kenya')
        self.assertEqual([region.slug for region in context['nav_region_groups'][0]['regions']], ['nairobi-environs', 'coastal-strip'])


class PackagePromotionTests(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.package = BasePackage.objects.create(
            title_en='Safari Circuit',
            title_de='Safari Rundreise',
            package_type=BasePackage.PackageType.SAFARI,
            duration_days=8,
            slug='safari-circuit',
        )
        PackagePricingSeason.objects.create(
            base_package=self.package,
            season_name='Peak',
            start_date=(self.now - timedelta(days=30)).date(),
            end_date=(self.now + timedelta(days=60)).date(),
            price_usd=1000,
        )

    def _promotion(self, **overrides):
        defaults = {
            'package': self.package,
            'label': 'Green Season',
            'discount_type': PackagePromotion.DiscountType.PERCENTAGE,
            'discount_value': Decimal('15'),
            'show_featured_badge': True,
            'show_in_banner': True,
            'is_active': True,
            'start_date': self.now - timedelta(days=1),
            'end_date': self.now + timedelta(days=10),
            'display_order': 0,
        }
        defaults.update(overrides)
        return PackagePromotion.objects.create(**defaults)

    def test_percentage_and_fixed_discount_math(self):
        percentage = type('P', (), {
            'discount_type': PackagePromotion.DiscountType.PERCENTAGE,
            'discount_value': Decimal('15'),
        })()
        fixed = type('P', (), {
            'discount_type': PackagePromotion.DiscountType.FIXED,
            'discount_value': Decimal('250'),
        })()

        self.assertEqual(apply_promotion(1000, percentage), (850, 150))
        self.assertEqual(apply_promotion(1000, fixed), (750, 250))

    def test_active_pricing_exposes_original_promo_and_savings(self):
        self._promotion()
        pricing = build_package_pricing(self.package)

        self.assertTrue(pricing['has_promo_price'])
        self.assertEqual(pricing['original_price'], 1000)
        self.assertEqual(pricing['promo_price'], 850)
        self.assertEqual(pricing['savings'], 150)
        self.assertEqual(pricing['starting_price_label'], 'From $850')
        self.assertEqual(pricing['original_price_label'], 'From $1,000')
        self.assertEqual(pricing['savings_label'], 'Save $150')
        self.assertEqual(pricing['promo_label'], 'Green Season')
        self.assertTrue(pricing['is_featured_promo'])

    def test_expired_promotions_stop_displaying(self):
        self._promotion(
            start_date=self.now - timedelta(days=20),
            end_date=self.now - timedelta(days=1),
        )

        pricing = build_package_pricing(self.package)
        self.assertFalse(pricing['has_promo_price'])
        self.assertEqual(featured_special_offer_cards(), [])
        self.assertEqual(package_promotion_banner_slides(), [])

    def test_featured_and_banner_surfaces(self):
        self._promotion()

        cards = featured_special_offer_cards()
        slides = package_promotion_banner_slides(language_code='de')

        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['package'].slug, 'safari-circuit')
        self.assertEqual(len(slides), 1)
        self.assertEqual(slides[0].title, 'Safari Rundreise')

        request = RequestFactory().get('/')
        request.LANGUAGE_CODE = 'de'
        context = active_promotional_banners(request)
        self.assertTrue(context['has_promotional_banners'])
        self.assertEqual(context['promotional_banners'][0].title, 'Safari Rundreise')

    def test_special_offers_priority_fill_and_limit(self):
        featured_pkg = self.package
        self._promotion(package=featured_pkg, label='Featured Deal', display_order=1)

        filler_a = BasePackage.objects.create(
            title_en='Golf Filler A',
            title_de='Golf Filler A',
            package_type=BasePackage.PackageType.GOLF,
            duration_days=6,
            slug='golf-filler-a',
        )
        PackagePricingSeason.objects.create(
            base_package=filler_a,
            season_name='Peak',
            start_date=(self.now - timedelta(days=30)).date(),
            end_date=(self.now + timedelta(days=60)).date(),
            price_usd=2000,
        )
        self._promotion(
            package=filler_a,
            label='Filler A',
            show_featured_badge=False,
            show_in_banner=False,
            display_order=2,
        )

        filler_b = BasePackage.objects.create(
            title_en='Golf Filler B',
            title_de='Golf Filler B',
            package_type=BasePackage.PackageType.GOLF,
            duration_days=7,
            slug='golf-filler-b',
        )
        PackagePricingSeason.objects.create(
            base_package=filler_b,
            season_name='Peak',
            start_date=(self.now - timedelta(days=30)).date(),
            end_date=(self.now + timedelta(days=60)).date(),
            price_usd=3000,
        )
        self._promotion(
            package=filler_b,
            label='Filler B',
            show_featured_badge=False,
            show_in_banner=False,
            display_order=3,
        )

        filler_c = BasePackage.objects.create(
            title_en='Golf Filler C',
            title_de='Golf Filler C',
            package_type=BasePackage.PackageType.GOLF_SAFARI,
            duration_days=9,
            slug='golf-filler-c',
        )
        PackagePricingSeason.objects.create(
            base_package=filler_c,
            season_name='Peak',
            start_date=(self.now - timedelta(days=30)).date(),
            end_date=(self.now + timedelta(days=60)).date(),
            price_usd=4000,
        )
        self._promotion(
            package=filler_c,
            label='Filler C',
            show_featured_badge=False,
            show_in_banner=False,
            display_order=4,
        )

        cards = featured_special_offer_cards(limit=3)
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0]['package'].slug, 'safari-circuit')
        self.assertEqual(
            [card['package'].slug for card in cards[1:]],
            ['golf-filler-a', 'golf-filler-b'],
        )

    def test_validation_rejects_invalid_discount_window(self):
        promo = PackagePromotion(
            package=self.package,
            label='Bad Window',
            discount_type=PackagePromotion.DiscountType.PERCENTAGE,
            discount_value=Decimal('15'),
            start_date=self.now + timedelta(days=5),
            end_date=self.now + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            promo.full_clean()
