from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .admin_mixins import (
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
)
from .models import (
    Accommodation,
    BasePackage,
    DayActivity,
    ExperienceFAQ,
    ExperienceOfferItem,
    GalleryImage,
    GolfCourse,
    GolfEvent,
    JournalArticle,
    PackageItineraryDay,
    PackagePricingSeason,
    PackagePromotion,
    Partner,
    PromotionalBanner,
    Region,
    RelatedExperience,
    SafariDestination,
    WellnessExperience,
)


# ---------------------------------------------------------------------------
# Shared experience inlines (gallery, FAQ, offers, related)
# ---------------------------------------------------------------------------


class GalleryImageInline(GenericTabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image_url', 'caption_en', 'caption_de', 'display_order')
    ordering = ('display_order', 'id')
    verbose_name_plural = 'Gallery images — HTTPS URLs shown on the public detail page'


class ExperienceFAQInline(GenericTabularInline):
    model = ExperienceFAQ
    extra = 1
    fields = ('question', 'answer', 'display_order')
    ordering = ('display_order', 'id')
    verbose_name_plural = 'FAQs — shown in the experience detail accordion'


class ExperienceOfferItemInline(GenericTabularInline):
    model = ExperienceOfferItem
    extra = 1
    fields = ('kind', 'label', 'display_order')
    ordering = ('kind', 'display_order', 'id')
    verbose_name_plural = 'Offer items — inclusions / highlights guests see on the page'


class RelatedExperienceInline(GenericTabularInline):
    model = RelatedExperience
    ct_field = 'from_content_type'
    ct_fk_field = 'from_object_id'
    extra = 0
    fields = (
        'to_content_type',
        'to_object_id',
        'label',
        'display_order',
    )
    ordering = ('display_order', 'id')
    verbose_name_plural = (
        'Related experiences — link other golf, safari, stay, or wellness pages '
        '(object ID = the related record’s database ID)'
    )


EXPERIENCE_INLINES = [
    GalleryImageInline,
    ExperienceOfferItemInline,
    ExperienceFAQInline,
    RelatedExperienceInline,
]


class ExperienceAdminBase(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
    admin.ModelAdmin,
):
    """Shared behaviour for destination experience editors."""

    save_on_top = True
    inlines = EXPERIENCE_INLINES
    autocomplete_fields = ('region',)
    field_placeholders = {
        'overview': 'Short guest-facing overview for cards and the top of the detail page',
        'hero_image_url': 'https://… full-bleed detail hero',
        'meta_title': 'Optional SEO title override',
        'meta_description': 'Optional SEO description (≈150–160 characters)',
        'slug': 'url-friendly-slug',
    }


# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------


@admin.register(Region)
class RegionAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
    admin.ModelAdmin,
):
    list_display = (
        'name_en',
        'name_de',
        'country_en',
        'slug',
        'is_active',
    )
    list_filter = ('is_active', 'country_en')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name_en',)}
    search_fields = (
        'name_en',
        'name_de',
        'slug',
        'country_en',
        'country_de',
        'description_en',
    )
    save_on_top = True
    inlines = (GalleryImageInline,)
    field_placeholders = {
        'name_en': 'e.g. Maasai Mara',
        'name_de': 'German region name',
        'country_en': 'e.g. Kenya',
        'description_en': 'Hub intro copy for the region page',
        'description_de': 'German hub intro',
        'slug': 'maasai-mara',
        'meta_title': 'Optional SEO title',
        'meta_description': 'Optional SEO description',
    }
    fieldsets = (
        (
            'Region identity',
            {
                'description': (
                    'Regions power the destinations dropdown, region hubs, and '
                    'experience filtering. Keep slugs stable once published.'
                ),
                'fields': (
                    'name_en',
                    'name_de',
                    'slug',
                    'country_en',
                    'country_de',
                    'description_en',
                    'description_de',
                    'is_active',
                ),
            },
        ),
        (
            'SEO',
            {
                'fields': (
                    'meta_title',
                    'meta_description',
                ),
            },
        ),
    )


# ---------------------------------------------------------------------------
# Packages — nested days + activities on one screen
# ---------------------------------------------------------------------------


class PackagePromotionInline(NestedStackedInline):
    model = PackagePromotion
    extra = 0
    classes = ('collapse',)
    fields = (
        'label',
        'discount_type',
        'discount_value',
        'is_active',
        'start_date',
        'end_date',
        'show_featured_badge',
        'show_in_banner',
        'banner_title',
        'banner_description',
        'banner_cta_text',
        'display_order',
    )
    ordering = ('display_order', '-start_date')
    verbose_name_plural = (
        'Promotions — Active + dates; Feature (Special Offers) and/or Banner '
        '(placement only — not a card badge)'
    )


class PackagePricingSeasonInline(NestedTabularInline):
    model = PackagePricingSeason
    extra = 1
    fields = ('season_name', 'start_date', 'end_date', 'price_usd')
    ordering = ('start_date',)
    verbose_name_plural = (
        'Pricing seasons — the lowest active season price becomes the “From” price'
    )


class DayActivityNestedInline(NestedTabularInline):
    model = DayActivity
    extra = 1
    fields = ('content_type', 'object_id', 'display_order')
    ordering = ('display_order', 'id')
    verbose_name = 'activity'
    verbose_name_plural = 'Activities for this day'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'object_id' and formfield is not None:
            formfield.help_text = (
                'Numeric ID of the golf course, safari destination, or wellness '
                'experience (open that changelist in another tab to copy the ID).'
            )
            formfield.widget.attrs.setdefault('placeholder', 'e.g. 12')
        if db_field.name == 'content_type' and formfield is not None:
            formfield.help_text = (
                'Choose Golf course, Safari destination, or Wellness experience.'
            )
        return formfield


class DayActivityInline(admin.TabularInline):
    """Non-nested twin for the standalone itinerary-day change page."""

    model = DayActivity
    extra = 1
    fields = ('content_type', 'object_id', 'display_order')
    ordering = ('display_order', 'id')
    verbose_name_plural = 'Day activities'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'object_id' and formfield is not None:
            formfield.help_text = (
                'Numeric ID of the linked golf, safari, or wellness record.'
            )
        return formfield


class PackageItineraryDayNestedInline(NestedStackedInline):
    model = PackageItineraryDay
    extra = 1
    fields = ('day_number', 'title_en', 'title_de', 'accommodation')
    autocomplete_fields = ('accommodation',)
    ordering = ('day_number',)
    inlines = (DayActivityNestedInline,)
    verbose_name = 'itinerary day'
    verbose_name_plural = (
        'Itinerary days — add Day 1, Day 2, … here and nest activities under each day'
    )


@admin.register(BasePackage)
class BasePackageAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
    NestedModelAdmin,
):
    list_display = (
        'title_en',
        'package_type',
        'duration_days',
        'day_count',
        'slug',
        'is_active',
        'view_on_site_link',
    )
    list_filter = ('package_type', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title_en',)}
    search_fields = ('title_en', 'title_de', 'slug', 'summary_en')
    save_on_top = True
    inlines = (
        PackagePricingSeasonInline,
        PackageItineraryDayNestedInline,
        PackagePromotionInline,
    )
    field_placeholders = {
        'title_en': 'e.g. 8-Day Amboseli Safari Escape',
        'title_de': 'German title for the de. site',
        'summary_en': 'Short guest-facing summary for cards and detail',
        'summary_de': 'German summary',
        'inclusions_en': 'One included item per line',
        'inclusions_de': 'One included item per line (German)',
        'exclusions_en': 'One excluded item per line',
        'exclusions_de': 'One excluded item per line (German)',
        'card_image_url': 'https://… listing / card image',
        'hero_image_url': 'https://… detail hero image',
        'slug': 'url-slug-for-this-journey',
    }
    fieldsets = (
        (
            'Journey identity',
            {
                'description': (
                    'Workflow: (1) fill identity + media and save — you stay on this '
                    'page, (2) add pricing seasons, (3) add itinerary days and nest '
                    'activities under each day, (4) optionally add promotions. '
                    'No need to leave this screen to build the itinerary.'
                ),
                'fields': (
                    'title_en',
                    'title_de',
                    'slug',
                    'package_type',
                    'duration_days',
                    'summary_en',
                    'summary_de',
                    'is_active',
                ),
            },
        ),
        (
            'Inclusions & exclusions',
            {
                'description': 'One item per line — rendered as lists on the journey detail page.',
                'fields': (
                    'inclusions_en',
                    'inclusions_de',
                    'exclusions_en',
                    'exclusions_de',
                ),
            },
        ),
        (
            'Media',
            {
                'description': (
                    'Full HTTPS image URLs. Card = listings / home; hero = journey detail.'
                ),
                'fields': (
                    'card_image_url',
                    'hero_image_url',
                ),
            },
        ),
    )

    @admin.display(description='Days built')
    def day_count(self, obj):
        return f'{obj.itinerary_days.count()} / {obj.duration_days}'

    @admin.display(description='Site')
    def view_on_site_link(self, obj):
        if not obj.slug:
            return '—'
        return format_html(
            '<a href="/journeys/{}/" target="_blank" rel="noopener">Open ↗</a>',
            obj.slug,
        )


@admin.register(PackageItineraryDay)
class PackageItineraryDayAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        'base_package',
        'day_number',
        'title_en',
        'accommodation',
        'activity_count',
    )
    list_filter = ('base_package__package_type',)
    search_fields = (
        'title_en',
        'title_de',
        'base_package__title_en',
        'base_package__slug',
    )
    autocomplete_fields = ('base_package', 'accommodation')
    ordering = ('base_package__title_en', 'day_number')
    save_on_top = True
    inlines = (DayActivityInline,)
    field_placeholders = {
        'title_en': 'e.g. Arrive Nairobi · Club practice',
        'title_de': 'German day title',
    }
    fieldsets = (
        (
            None,
            {
                'description': (
                    'Prefer editing days from the parent Journey page (nested). '
                    'Use this screen to deep-edit one day or repair activities.'
                ),
                'fields': (
                    'base_package',
                    'day_number',
                    'title_en',
                    'title_de',
                    'accommodation',
                ),
            },
        ),
    )

    @admin.display(description='Activities')
    def activity_count(self, obj):
        return obj.activities.count()


@admin.register(DayActivity)
class DayActivityAdmin(admin.ModelAdmin):
    list_display = (
        'itinerary_day',
        'content_type',
        'object_id',
        'display_order',
    )
    list_filter = ('content_type',)
    search_fields = (
        'itinerary_day__title_en',
        'itinerary_day__base_package__title_en',
    )
    autocomplete_fields = ('itinerary_day',)
    ordering = (
        'itinerary_day__base_package__title_en',
        'itinerary_day__day_number',
        'display_order',
    )
    fieldsets = (
        (
            None,
            {
                'description': (
                    'Usually managed under Journey → Itinerary day. '
                    'content_type picks the experience kind; object_id is that '
                    'record’s numeric ID in admin.'
                ),
                'fields': (
                    'itinerary_day',
                    'content_type',
                    'object_id',
                    'display_order',
                ),
            },
        ),
    )


@admin.register(PackagePromotion)
class PackagePromotionAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        'label',
        'package',
        'discount_type',
        'discount_value',
        'show_featured_badge',
        'show_in_banner',
        'is_active',
        'start_date',
        'end_date',
        'display_order',
    )
    list_filter = (
        'discount_type',
        'show_featured_badge',
        'show_in_banner',
        'is_active',
        'package__package_type',
        'start_date',
    )
    search_fields = (
        'label',
        'package__title_en',
        'package__slug',
        'banner_title',
    )
    list_editable = (
        'is_active',
        'display_order',
        'show_featured_badge',
        'show_in_banner',
    )
    autocomplete_fields = ('package',)
    save_on_top = True
    field_placeholders = {
        'label': 'e.g. Green Season Escape',
        'banner_title': 'Optional banner headline override',
        'banner_description': 'Optional banner supporting line',
        'banner_cta_text': 'e.g. View Offer',
    }
    fieldsets = (
        (
            'Offer basics',
            {
                'description': (
                    'Create the discount first, then complete the visibility '
                    'checklist so the offer appears correctly on the site.'
                ),
                'fields': (
                    'package',
                    'label',
                    'discount_type',
                    'discount_value',
                ),
            },
        ),
        (
            'Checklist — visibility',
            {
                'description': (
                    'Required: Active + start/end dates that include today. '
                    'Then optionally Feature (Special Offers placement) and/or '
                    'Banner (top site banner). These are placement controls, '
                    'not card badges.'
                ),
                'fields': (
                    'is_active',
                    'start_date',
                    'end_date',
                    'show_featured_badge',
                    'show_in_banner',
                ),
            },
        ),
        (
            'Banner copy (optional)',
            {
                'description': (
                    'Only when Banner is checked. Leave blank to use the package '
                    'title, promo label, and “View Offer”.'
                ),
                'fields': (
                    'banner_title',
                    'banner_description',
                    'banner_cta_text',
                    'display_order',
                ),
                'classes': ('collapse',),
            },
        ),
    )


@admin.register(PackagePricingSeason)
class PackagePricingSeasonAdmin(admin.ModelAdmin):
    list_display = (
        'base_package',
        'season_name',
        'start_date',
        'end_date',
        'price_usd',
    )
    list_filter = ('base_package__package_type',)
    search_fields = ('season_name', 'base_package__title_en', 'base_package__slug')
    autocomplete_fields = ('base_package',)
    ordering = ('base_package__title_en', 'start_date')
    fieldsets = (
        (
            None,
            {
                'description': (
                    'Prefer adding seasons on the Journey page. Guests see the '
                    'lowest overlapping season price as the starting “From” price.'
                ),
                'fields': (
                    'base_package',
                    'season_name',
                    'start_date',
                    'end_date',
                    'price_usd',
                ),
            },
        ),
    )


# ---------------------------------------------------------------------------
# Journal, partners, events
# ---------------------------------------------------------------------------


@admin.register(JournalArticle)
class JournalArticleAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
    admin.ModelAdmin,
):
    list_display = (
        'title_en',
        'author',
        'category_en',
        'status',
        'published_at',
        'reading_time_minutes',
        'is_featured',
        'is_active',
    )
    list_filter = ('status', 'is_active', 'is_featured', 'published_at', 'category_en')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title_en',)}
    search_fields = (
        'title_en',
        'title_de',
        'slug',
        'author',
        'category_en',
        'tags',
        'excerpt_en',
    )
    filter_horizontal = ('related_articles',)
    readonly_fields = ('reading_time_minutes',)
    save_on_top = True
    field_placeholders = {
        'author': 'e.g. AfroLink Editorial',
        'category_en': 'e.g. Safari Notes',
        'tags': 'comma,separated,tags',
        'excerpt_en': 'Short teaser for cards and listings',
        'hero_image_url': 'https://… article hero',
        'youtube_url': 'https://www.youtube.com/watch?v=… or youtu.be/…',
        'meta_title': 'Optional SEO title',
        'meta_description': 'Optional SEO description',
    }
    fieldsets = (
        (
            'Article',
            {
                'description': (
                    'Set status to Published and add published_at for the article '
                    'to appear on the Journal.'
                ),
                'fields': (
                    'title_en',
                    'title_de',
                    'slug',
                    'author',
                    'category_en',
                    'category_de',
                    'tags',
                    'status',
                    'is_featured',
                    'is_active',
                    'published_at',
                    'reading_time_minutes',
                ),
            },
        ),
        (
            'Content',
            {
                'fields': (
                    'excerpt_en',
                    'excerpt_de',
                    'body_en',
                    'body_de',
                    'hero_image_url',
                    'youtube_url',
                ),
                'description': (
                    'Paste a standard or shortened YouTube link to embed a '
                    'responsive video in the article body.'
                ),
            },
        ),
        (
            'SEO',
            {'fields': ('meta_title', 'meta_description')},
        ),
        (
            'Related articles',
            {'fields': ('related_articles',)},
        ),
    )


@admin.register(Partner)
class PartnerAdmin(
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
    admin.ModelAdmin,
):
    list_display = ('name', 'display_order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('display_order', 'is_active')
    search_fields = ('name', 'logo_path')
    ordering = ('display_order', 'name')
    field_placeholders = {
        'name': 'Partner or brand name',
        'logo_path': 'Static path or full URL to logo',
    }
    fieldsets = (
        (
            None,
            {
                'description': 'Partners appear in the homepage trust / partners strip.',
                'fields': ('name', 'logo_path', 'display_order', 'is_active'),
            },
        ),
    )


@admin.register(GolfEvent)
class GolfEventAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    SoftActiveListFilterMixin,
    admin.ModelAdmin,
):
    list_display = (
        'title_en',
        'region',
        'event_date',
        'format_label',
        'recurrence',
        'accepts_inquiries',
        'is_promoted',
        'promotion_priority',
        'is_active',
    )
    list_filter = (
        'is_active',
        'accepts_inquiries',
        'is_promoted',
        'region',
        'recurrence',
        'event_date',
    )
    list_editable = ('accepts_inquiries', 'is_promoted', 'promotion_priority')
    prepopulated_fields = {'slug': ('title_en',)}
    search_fields = (
        'title_en',
        'title_de',
        'slug',
        'summary_en',
        'description_en',
        'format_label',
    )
    autocomplete_fields = ('region', 'golf_course')
    save_on_top = True
    field_placeholders = {
        'format_label': 'e.g. Stableford · 18 holes',
        'duration_label': 'e.g. Half day',
        'summary_en': 'Short listing summary',
        'image_url': 'https://… event image',
        'registration_url': 'https://… optional external registration',
    }
    fieldsets = (
        (
            'Event',
            {
                'description': (
                    'Promoted events can appear on the homepage. '
                    '“Accepts inquiries” controls whether guests can shortlist the event.'
                ),
                'fields': (
                    'title_en',
                    'title_de',
                    'slug',
                    'region',
                    'golf_course',
                    'format_label',
                    'duration_label',
                    'is_active',
                    'is_promoted',
                    'promotion_priority',
                    'accepts_inquiries',
                ),
            },
        ),
        (
            'Schedule',
            {
                'fields': (
                    'event_date',
                    'end_date',
                    'start_time',
                    'recurrence',
                    'recurrence_weekday',
                ),
            },
        ),
        (
            'Content',
            {
                'fields': (
                    'summary_en',
                    'summary_de',
                    'description_en',
                    'description_de',
                    'image_url',
                    'venue_notes',
                    'dress_code',
                    'eligibility_notes',
                    'inclusions',
                    'need_to_know',
                    'registration_url',
                ),
            },
        ),
        (
            'SEO',
            {'fields': ('meta_title', 'meta_description')},
        ),
    )


# ---------------------------------------------------------------------------
# Destination experiences
# ---------------------------------------------------------------------------


@admin.register(Accommodation)
class AccommodationAdmin(ExperienceAdminBase):
    list_display = (
        'name',
        'region',
        'property_type',
        'star_rating',
        'is_featured',
        'is_active',
    )
    list_filter = ('is_active', 'is_featured', 'region', 'property_type', 'star_rating')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'best_for', 'room_style', 'overview')
    fieldsets = (
        (
            'Overview',
            {
                'description': (
                    'Stays used on journey itinerary days and region hubs. '
                    'Featured stays can be prioritised in listings.'
                ),
                'fields': (
                    'region',
                    'name',
                    'slug',
                    'property_type',
                    'star_rating',
                    'overview',
                    'description_en',
                    'description_de',
                    'style',
                    'atmosphere',
                    'ideal_guests',
                    'best_for',
                    'is_featured',
                    'is_active',
                ),
            },
        ),
        (
            'Rooms',
            {
                'fields': (
                    'room_style',
                    'room_categories',
                    'occupancy',
                    'bed_types',
                    'room_size',
                    'has_balcony',
                    'room_view',
                ),
            },
        ),
        (
            'Amenities',
            {
                'fields': (
                    'has_pool',
                    'has_gym',
                    'has_spa',
                    'has_restaurant',
                    'has_bar',
                    'has_concierge',
                    'has_business_centre',
                    'has_wifi',
                    'amenities_json',
                ),
            },
        ),
        (
            'Dining',
            {
                'fields': (
                    'dining_wellness',
                    'restaurants',
                    'breakfast_included',
                    'private_dining',
                    'dietary_options',
                ),
            },
        ),
        (
            'Logistics & policies',
            {
                'fields': (
                    'location_access',
                    'distance_from_airport',
                    'latitude',
                    'longitude',
                    'check_in_time',
                    'check_out_time',
                    'early_check_in',
                    'late_check_out',
                    'family_friendly',
                    'adults_only',
                    'accessibility_notes',
                    'smoking_policy',
                    'pet_policy',
                    'need_to_know',
                ),
            },
        ),
        (
            'SEO & media',
            {
                'fields': (
                    'hero_image_url',
                    'meta_title',
                    'meta_description',
                ),
            },
        ),
    )


@admin.register(GolfCourse)
class GolfCourseAdmin(ExperienceAdminBase):
    list_display = (
        'name',
        'region',
        'course_style',
        'is_championship',
        'is_featured',
        'is_active',
    )
    list_filter = (
        'is_active',
        'is_featured',
        'is_championship',
        'course_style',
        'region',
    )
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'holes_and_par', 'difficulty_level', 'overview')
    fieldsets = (
        (
            'Overview',
            {
                'description': (
                    'Courses can be linked as day activities on journeys and shown '
                    'on region hubs.'
                ),
                'fields': (
                    'region',
                    'name',
                    'slug',
                    'overview',
                    'course_style',
                    'architect_designer',
                    'year_opened',
                    'is_championship',
                    'is_featured',
                    'is_active',
                ),
            },
        ),
        (
            'Course details',
            {
                'fields': (
                    'holes_and_par',
                    'holes',
                    'par',
                    'course_length',
                    'turf_grass_type',
                    'signature_features',
                    'signature_holes',
                    'difficulty_level',
                    'best_suited_for',
                ),
            },
        ),
        (
            'Facilities',
            {
                'fields': (
                    'practice_range',
                    'putting_green',
                    'short_game_area',
                    'golf_academy',
                    'clubhouse',
                    'restaurant',
                    'pro_shop',
                    'walking_allowed',
                    'golf_carts',
                    'caddies',
                    'rental_clubs',
                    'locker_rooms',
                    'changing_rooms',
                    'facilities',
                ),
            },
        ),
        (
            'Tee times & seasons',
            {
                'fields': (
                    'booking_window',
                    'average_playing_time',
                    'peak_season',
                    'best_playing_months',
                    'best_time_to_play',
                    'booking_notes',
                ),
            },
        ),
        (
            'Dress & preparation',
            {
                'fields': (
                    'collared_shirts_required',
                    'soft_spikes_required',
                    'denim_allowed',
                    'dress_code',
                    'arrival_notes',
                ),
            },
        ),
        (
            'Logistics',
            {
                'fields': (
                    'distance_from_airport',
                    'latitude',
                    'longitude',
                ),
            },
        ),
        (
            'SEO & media',
            {
                'fields': (
                    'hero_image_url',
                    'meta_title',
                    'meta_description',
                ),
            },
        ),
    )


@admin.register(SafariDestination)
class SafariDestinationAdmin(ExperienceAdminBase):
    list_display = (
        'name',
        'region',
        'big_five_available',
        'is_featured',
        'is_active',
    )
    list_filter = (
        'is_active',
        'is_featured',
        'big_five_available',
        'region',
    )
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug', 'key_wildlife', 'experience_style', 'overview')
    fieldsets = (
        (
            'Overview',
            {
                'description': (
                    'Safari destinations are parks / conservancies guests visit. '
                    'Link them as day activities on journeys.'
                ),
                'fields': (
                    'region',
                    'name',
                    'slug',
                    'overview',
                    'history',
                    'conservation_significance',
                    'landscape_description',
                    'experience_style',
                    'typical_duration',
                    'is_featured',
                    'is_active',
                ),
            },
        ),
        (
            'Wildlife',
            {
                'fields': (
                    'key_wildlife',
                    'big_five_available',
                    'common_wildlife',
                    'rare_wildlife',
                    'birdwatching',
                    'seasonal_migration',
                    'photography_opportunities',
                ),
            },
        ),
        (
            'Visitor experiences',
            {
                'fields': (
                    'game_drives',
                    'walking_safaris',
                    'night_drives',
                    'boat_safaris',
                    'balloon_safaris',
                    'guided_tours',
                    'self_drive_allowed',
                ),
            },
        ),
        (
            'Seasons',
            {
                'fields': (
                    'best_season',
                    'peak_season',
                    'green_season',
                    'migration_season',
                    'best_months',
                ),
            },
        ),
        (
            'Logistics',
            {
                'fields': (
                    'distance_from_airport',
                    'driving_time',
                    'internal_flights_available',
                    'park_opening_hours',
                    'access_notes',
                    'latitude',
                    'longitude',
                ),
            },
        ),
        (
            'Preparation',
            {
                'fields': (
                    'clothing_recommendations',
                    'weather_notes',
                    'camera_recommendations',
                    'luggage_recommendations',
                    'park_regulations',
                    'packing_notes',
                    'conservation_notes',
                    'need_to_know',
                ),
            },
        ),
        (
            'SEO & media',
            {
                'fields': (
                    'hero_image_url',
                    'meta_title',
                    'meta_description',
                ),
            },
        ),
    )


@admin.register(WellnessExperience)
class WellnessExperienceAdmin(ExperienceAdminBase):
    list_display = (
        'name_en',
        'region',
        'category',
        'is_featured',
        'is_active',
    )
    list_filter = ('is_active', 'is_featured', 'category', 'region')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name_en',)}
    search_fields = (
        'name_en',
        'name_de',
        'slug',
        'treatment_style',
        'ideal_for',
        'overview',
    )
    fieldsets = (
        (
            'Overview',
            {
                'description': (
                    'Wellness experiences appear on region hubs and can be linked '
                    'as journey day activities.'
                ),
                'fields': (
                    'region',
                    'name_en',
                    'name_de',
                    'slug',
                    'category',
                    'overview',
                    'wellness_purpose',
                    'treatment_style',
                    'ideal_for',
                    'is_featured',
                    'is_active',
                ),
            },
        ),
        (
            'Treatments & facilities',
            {
                'fields': (
                    'has_massage',
                    'has_hydrotherapy',
                    'has_sauna',
                    'has_steam_room',
                    'has_yoga',
                    'has_meditation',
                    'has_fitness',
                    'has_pool',
                    'has_spa',
                    'has_gym',
                    'has_relaxation_lounge',
                    'has_private_treatment_rooms',
                    'inclusions',
                ),
            },
        ),
        (
            'Duration & preparation',
            {
                'fields': (
                    'typical_duration',
                    'duration_choice',
                    'arrival_time',
                    'clothing_notes',
                    'preparation_notes',
                    'suitability_notes',
                    'medical_considerations',
                    'age_restrictions',
                    'health_notice',
                ),
            },
        ),
        (
            'SEO & media',
            {
                'fields': (
                    'hero_image_url',
                    'meta_title',
                    'meta_description',
                ),
            },
        ),
    )


# ---------------------------------------------------------------------------
# Promotional banners (manual CMS slides)
# ---------------------------------------------------------------------------


@admin.register(PromotionalBanner)
class PromotionalBannerAdmin(
    ContinueEditingMixin,
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        'title',
        'promotion_type',
        'is_active',
        'start_date',
        'end_date',
        'display_order',
        'is_dismissible',
        'updated_at',
    )
    list_filter = ('promotion_type', 'is_active', 'is_dismissible', 'start_date')
    search_fields = ('title', 'short_description', 'cta_text', 'cta_url')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order', '-start_date')
    save_on_top = True
    field_placeholders = {
        'title': 'Banner headline',
        'short_description': 'One supporting sentence',
        'cta_text': 'e.g. View Journey',
        'cta_url': '/journeys/your-package-slug/',
        'background_image_url': 'https://… optional banner background',
    }
    fieldsets = (
        (
            'Banner content',
            {
                'description': (
                    'Manual top-of-site slides. For a featured journey, set CTA URL '
                    'to /journeys/your-package-slug/ — not /journeys/. '
                    'Package promotions with “Show in banner” are added automatically '
                    'and already link to the correct detail page.'
                ),
                'fields': (
                    'title',
                    'short_description',
                    'promotion_type',
                    'cta_text',
                    'cta_url',
                    'background_image_url',
                ),
            },
        ),
        (
            'Scheduling',
            {
                'fields': (
                    'is_active',
                    'start_date',
                    'end_date',
                    'display_order',
                    'is_dismissible',
                ),
            },
        ),
    )


# Inline-only models are not registered at the top level to reduce sidebar clutter:
# GalleryImage, ExperienceFAQ, ExperienceOfferItem, RelatedExperience
