from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


def line_items(value):
    return [item.strip() for item in value.splitlines() if item.strip()]


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(TimeStampedModel):
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class ExperienceRelationsMixin(models.Model):
    """Shared gallery / FAQ / offer / related links for experience models."""

    gallery_images = GenericRelation(
        'GalleryImage',
        content_type_field='content_type',
        object_id_field='object_id',
    )
    faqs = GenericRelation(
        'ExperienceFAQ',
        content_type_field='content_type',
        object_id_field='object_id',
    )
    offer_items = GenericRelation(
        'ExperienceOfferItem',
        content_type_field='content_type',
        object_id_field='object_id',
    )

    class Meta:
        abstract = True

    def get_included_items(self):
        return self.offer_items.filter(
            kind=ExperienceOfferItem.Kind.INCLUDED
        ).order_by('display_order', 'id')

    def get_optional_items(self):
        return self.offer_items.filter(
            kind=ExperienceOfferItem.Kind.OPTIONAL
        ).order_by('display_order', 'id')

    def get_related_links(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return RelatedExperience.objects.filter(
            from_content_type=content_type,
            from_object_id=self.pk,
        ).select_related('to_content_type').order_by('display_order', 'id')


class Region(SoftDeleteModel):
    name_en = models.CharField(max_length=255)
    name_de = models.CharField(max_length=255)
    country_en = models.CharField(max_length=255, blank=True, default='')
    country_de = models.CharField(max_length=255, blank=True, default='')
    description_en = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    gallery_images = GenericRelation(
        'GalleryImage',
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='region',
    )

    class Meta:
        ordering = ['name_en']

    def __str__(self):
        return self.name_en

    def get_country_name(self, language_code='en'):
        if language_code == 'de':
            return self.country_de or self.country_en or ''
        return self.country_en or self.country_de or ''


class Accommodation(ExperienceRelationsMixin, SoftDeleteModel):
    class PropertyType(models.TextChoices):
        HOTEL = 'hotel', 'Hotel'
        SAFARI_LODGE = 'safari_lodge', 'Safari Lodge'
        GOLF_RESORT = 'golf_resort', 'Golf Resort'
        BOUTIQUE = 'boutique', 'Boutique Hotel'
        VILLA = 'villa', 'Villa'

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='accommodations',
        db_index=True,
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    property_type = models.CharField(
        max_length=40,
        choices=PropertyType.choices,
        blank=True,
        db_index=True,
    )
    star_rating = models.PositiveSmallIntegerField()
    description_en = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    style = models.CharField(max_length=255, blank=True)
    atmosphere = models.CharField(max_length=255, blank=True)
    ideal_guests = models.CharField(max_length=255, blank=True)
    room_style = models.CharField(max_length=255, blank=True)
    room_categories = models.TextField(
        blank=True,
        help_text='One room category per line.',
    )
    occupancy = models.CharField(max_length=150, blank=True)
    bed_types = models.CharField(max_length=255, blank=True)
    room_size = models.CharField(max_length=100, blank=True)
    has_balcony = models.BooleanField(default=False)
    room_view = models.CharField(max_length=255, blank=True)
    best_for = models.CharField(max_length=255, blank=True)
    location_access = models.TextField(blank=True)
    distance_from_airport = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    dining_wellness = models.TextField(blank=True)
    restaurants = models.TextField(blank=True)
    breakfast_included = models.BooleanField(default=False)
    private_dining = models.BooleanField(default=False)
    dietary_options = models.TextField(blank=True)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_bar = models.BooleanField(default=False)
    has_concierge = models.BooleanField(default=False)
    has_business_centre = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=True)
    check_in_time = models.CharField(max_length=50, blank=True)
    check_out_time = models.CharField(max_length=50, blank=True)
    early_check_in = models.BooleanField(default=False)
    late_check_out = models.BooleanField(default=False)
    family_friendly = models.BooleanField(default=True)
    adults_only = models.BooleanField(default=False)
    accessibility_notes = models.TextField(blank=True)
    smoking_policy = models.CharField(max_length=255, blank=True)
    pet_policy = models.CharField(max_length=255, blank=True)
    need_to_know = models.TextField(
        blank=True,
        help_text='One practical guest note per line.',
    )
    amenities_json = models.JSONField(default=dict, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    hero_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['region__name_en', 'name']
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodations'

    def __str__(self):
        return self.name

    def get_need_to_know(self):
        return line_items(self.need_to_know)

    def get_room_categories(self):
        return line_items(self.room_categories)

    def get_hero_image_url(self):
        if self.hero_image_url:
            return self.hero_image_url
        image = self.gallery_images.first()
        return image.image_url if image else ''


class GolfCourse(ExperienceRelationsMixin, SoftDeleteModel):
    class CourseStyle(models.TextChoices):
        PARKLAND = 'parkland', 'Parkland'
        LINKS = 'links', 'Links'
        RESORT = 'resort', 'Resort'
        MOUNTAIN = 'mountain', 'Mountain'

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='golf_courses',
        db_index=True,
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    overview = models.TextField(blank=True)
    holes_and_par = models.CharField(max_length=100, blank=True)
    holes = models.PositiveSmallIntegerField(blank=True, null=True)
    par = models.PositiveSmallIntegerField(blank=True, null=True)
    course_length = models.CharField(max_length=100, blank=True)
    architect_designer = models.CharField(max_length=255, blank=True)
    year_opened = models.PositiveSmallIntegerField(blank=True, null=True)
    course_style = models.CharField(
        max_length=40,
        choices=CourseStyle.choices,
        blank=True,
        db_index=True,
    )
    turf_grass_type = models.CharField(max_length=255, blank=True)
    signature_features = models.TextField(blank=True)
    signature_holes = models.TextField(blank=True)
    difficulty_level = models.CharField(max_length=150, blank=True)
    best_suited_for = models.CharField(max_length=255, blank=True)
    best_time_to_play = models.CharField(max_length=255, blank=True)
    is_championship = models.BooleanField(default=False, db_index=True)
    practice_range = models.BooleanField(default=False)
    putting_green = models.BooleanField(default=False)
    short_game_area = models.BooleanField(default=False)
    golf_academy = models.BooleanField(default=False)
    clubhouse = models.BooleanField(default=True)
    restaurant = models.BooleanField(default=False)
    pro_shop = models.BooleanField(default=False)
    walking_allowed = models.BooleanField(default=True)
    golf_carts = models.BooleanField(default=False)
    caddies = models.BooleanField(default=False)
    rental_clubs = models.BooleanField(default=False)
    locker_rooms = models.BooleanField(default=False)
    changing_rooms = models.BooleanField(default=False)
    booking_window = models.CharField(max_length=255, blank=True)
    average_playing_time = models.CharField(max_length=100, blank=True)
    peak_season = models.CharField(max_length=255, blank=True)
    best_playing_months = models.CharField(max_length=255, blank=True)
    collared_shirts_required = models.BooleanField(default=True)
    soft_spikes_required = models.BooleanField(default=True)
    denim_allowed = models.BooleanField(default=False)
    dress_code = models.TextField(blank=True)
    facilities = models.TextField(
        blank=True,
        help_text='One course facility or service per line.',
    )
    booking_notes = models.TextField(blank=True)
    arrival_notes = models.TextField(blank=True)
    distance_from_airport = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    hero_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['region__name_en', 'name']
        verbose_name = 'Golf Course'
        verbose_name_plural = 'Golf Courses'

    def __str__(self):
        return self.name

    def get_facilities(self):
        return line_items(self.facilities)

    def get_hero_image_url(self):
        if self.hero_image_url:
            return self.hero_image_url
        image = self.gallery_images.first()
        return image.image_url if image else ''


class SafariDestination(ExperienceRelationsMixin, SoftDeleteModel):
    """A safari place guests visit (park/reserve/conservancy), not a lodge."""

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='safari_destinations',
        db_index=True,
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    overview = models.TextField(blank=True)
    history = models.TextField(blank=True)
    conservation_significance = models.TextField(blank=True)
    landscape_description = models.TextField(blank=True)
    key_wildlife = models.TextField(blank=True)
    big_five_available = models.BooleanField(default=False)
    common_wildlife = models.TextField(blank=True)
    rare_wildlife = models.TextField(blank=True)
    birdwatching = models.BooleanField(default=False)
    seasonal_migration = models.BooleanField(default=False)
    photography_opportunities = models.TextField(blank=True)
    game_drives = models.BooleanField(default=True)
    walking_safaris = models.BooleanField(default=False)
    night_drives = models.BooleanField(default=False)
    boat_safaris = models.BooleanField(default=False)
    balloon_safaris = models.BooleanField(default=False)
    guided_tours = models.BooleanField(default=True)
    self_drive_allowed = models.BooleanField(default=False)
    best_season = models.CharField(max_length=255, blank=True)
    peak_season = models.CharField(max_length=255, blank=True)
    green_season = models.CharField(max_length=255, blank=True)
    migration_season = models.CharField(max_length=255, blank=True)
    best_months = models.CharField(max_length=255, blank=True)
    typical_duration = models.CharField(max_length=150, blank=True)
    experience_style = models.CharField(max_length=255, blank=True)
    distance_from_airport = models.CharField(max_length=255, blank=True)
    driving_time = models.CharField(max_length=255, blank=True)
    internal_flights_available = models.BooleanField(default=False)
    park_opening_hours = models.CharField(max_length=255, blank=True)
    access_notes = models.TextField(blank=True)
    clothing_recommendations = models.TextField(blank=True)
    weather_notes = models.TextField(blank=True)
    camera_recommendations = models.TextField(blank=True)
    luggage_recommendations = models.TextField(blank=True)
    park_regulations = models.TextField(blank=True)
    packing_notes = models.TextField(blank=True)
    conservation_notes = models.TextField(blank=True)
    need_to_know = models.TextField(
        blank=True,
        help_text='One practical safari guest note per line.',
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    hero_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['region__name_en', 'name']
        db_table = 'destination_cms_safariextension'
        verbose_name = 'Safari Destination'
        verbose_name_plural = 'Safari Destinations'

    def __str__(self):
        return self.name

    def get_need_to_know(self):
        return line_items(self.need_to_know)

    def get_hero_image_url(self):
        if self.hero_image_url:
            return self.hero_image_url
        image = self.gallery_images.first()
        return image.image_url if image else ''


# Backward-compatible alias for imports and inquiry FK target.
SafariExtension = SafariDestination


class WellnessExperience(ExperienceRelationsMixin, SoftDeleteModel):
    class DurationChoice(models.TextChoices):
        SIXTY_MIN = '60_min', '60 minutes'
        HALF_DAY = 'half_day', 'Half day'
        FULL_DAY = 'full_day', 'Full day'
        MULTI_DAY = 'multi_day', 'Multi-day'

    class Category(models.TextChoices):
        SPA = 'spa', 'Spa'
        RECOVERY = 'recovery', 'Recovery'
        YOGA = 'yoga', 'Yoga / Retreat'
        MASSAGE = 'massage', 'Massage'
        THERMAL = 'thermal', 'Thermal Spa'
        OTHER = 'other', 'Other'

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='wellness_experiences',
        db_index=True,
    )
    name_en = models.CharField(max_length=255)
    name_de = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    category = models.CharField(
        max_length=40,
        choices=Category.choices,
        blank=True,
        db_index=True,
    )
    overview = models.TextField(blank=True)
    wellness_purpose = models.TextField(blank=True)
    typical_duration = models.CharField(max_length=150, blank=True)
    duration_choice = models.CharField(
        max_length=40,
        choices=DurationChoice.choices,
        blank=True,
    )
    treatment_style = models.CharField(max_length=255, blank=True)
    ideal_for = models.CharField(max_length=255, blank=True)
    has_massage = models.BooleanField(default=False)
    has_hydrotherapy = models.BooleanField(default=False)
    has_sauna = models.BooleanField(default=False)
    has_steam_room = models.BooleanField(default=False)
    has_yoga = models.BooleanField(default=False)
    has_meditation = models.BooleanField(default=False)
    has_fitness = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_relaxation_lounge = models.BooleanField(default=False)
    has_private_treatment_rooms = models.BooleanField(default=False)
    inclusions = models.TextField(
        blank=True,
        help_text='One wellness inclusion per line.',
    )
    preparation_notes = models.TextField(blank=True)
    arrival_time = models.CharField(max_length=150, blank=True)
    clothing_notes = models.TextField(blank=True)
    suitability_notes = models.TextField(blank=True)
    medical_considerations = models.TextField(blank=True)
    age_restrictions = models.CharField(max_length=255, blank=True)
    health_notice = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    hero_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['region__name_en', 'name_en']
        verbose_name = 'Wellness Experience'
        verbose_name_plural = 'Wellness Experiences'

    def __str__(self):
        return self.name_en

    def get_inclusions(self):
        return line_items(self.inclusions)

    def get_hero_image_url(self):
        if self.hero_image_url:
            return self.hero_image_url
        image = self.gallery_images.first()
        return image.image_url if image else ''


class GalleryImage(TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    image_url = models.URLField(max_length=500)
    caption_en = models.CharField(max_length=255, blank=True)
    caption_de = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['display_order', 'created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['content_type', 'object_id', 'display_order']),
        ]

    def __str__(self):
        return f'{self.content_type} image #{self.pk}'


class ExperienceFAQ(TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Experience FAQ'
        verbose_name_plural = 'Experience FAQs'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.question


class ExperienceOfferItem(TimeStampedModel):
    class Kind(models.TextChoices):
        INCLUDED = 'included', 'Included'
        OPTIONAL = 'optional', 'Optional Extra'

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    kind = models.CharField(
        max_length=20,
        choices=Kind.choices,
        db_index=True,
    )
    label = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['kind', 'display_order', 'id']
        verbose_name = 'Experience Offer Item'
        verbose_name_plural = 'Experience Offer Items'
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'kind']),
        ]

    def __str__(self):
        return f'{self.kind}: {self.label}'


class RelatedExperience(TimeStampedModel):
    from_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='related_from',
        db_index=True,
    )
    from_object_id = models.PositiveBigIntegerField(db_index=True)
    from_object = GenericForeignKey('from_content_type', 'from_object_id')
    to_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='related_to',
        db_index=True,
    )
    to_object_id = models.PositiveBigIntegerField(db_index=True)
    to_object = GenericForeignKey('to_content_type', 'to_object_id')
    label = models.CharField(max_length=100, blank=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Related Experience'
        verbose_name_plural = 'Related Experiences'
        indexes = [
            models.Index(fields=['from_content_type', 'from_object_id']),
            models.Index(fields=['to_content_type', 'to_object_id']),
        ]

    def __str__(self):
        return self.label or f'Related #{self.pk}'


class JournalArticle(SoftDeleteModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title_en = models.CharField(max_length=255)
    title_de = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    author = models.CharField(max_length=120, blank=True, default='AfroLink Adventures')
    category_en = models.CharField(max_length=100, blank=True)
    category_de = models.CharField(max_length=100, blank=True)
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text='Comma-separated tags, e.g. golf, safari, wellness',
    )
    excerpt_en = models.TextField(blank=True)
    excerpt_de = models.TextField(blank=True)
    body_en = models.TextField(help_text='Article body in Markdown.')
    body_de = models.TextField(blank=True, help_text='German body in Markdown.')
    hero_image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Featured image URL used on listing and detail pages.',
    )
    youtube_url = models.CharField(
        max_length=500,
        blank=True,
        help_text=(
            'Optional YouTube URL to embed in the article. '
            'Accepts youtube.com/watch, youtu.be, /embed, and /shorts links.'
        ),
    )
    published_at = models.DateField(db_index=True)
    reading_time_minutes = models.PositiveIntegerField(
        default=1,
        help_text='Auto-calculated from English Markdown word count on save.',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        db_index=True,
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    related_articles = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='related_from',
    )

    class Meta:
        ordering = ['-published_at', 'title_en']

    def __str__(self):
        return self.title_en

    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def get_youtube_video_id(self):
        from .youtube import extract_youtube_video_id

        return extract_youtube_video_id(self.youtube_url)

    def get_youtube_embed_url(self):
        from .youtube import youtube_embed_url

        return youtube_embed_url(self.youtube_url)

    def clean(self):
        from django.core.exceptions import ValidationError

        from .youtube import extract_youtube_video_id

        super().clean()
        if self.youtube_url and not extract_youtube_video_id(self.youtube_url):
            raise ValidationError(
                {
                    'youtube_url': (
                        'Enter a valid YouTube URL '
                        '(youtube.com/watch, youtu.be, /embed, or /shorts).'
                    ),
                }
            )

    def calculate_reading_time(self):
        import math
        import re

        words = len(re.findall(r"\w+", self.body_en or ''))
        return max(1, math.ceil(words / 200))

    def save(self, *args, **kwargs):
        from .youtube import extract_youtube_video_id

        self.youtube_url = (self.youtube_url or '').strip()
        # Outside ModelForm, clear invalid values instead of raising so
        # programmatic saves stay resilient; admin forms still use clean().
        if self.youtube_url and not extract_youtube_video_id(self.youtube_url):
            self.youtube_url = ''
        self.reading_time_minutes = self.calculate_reading_time()
        super().save(*args, **kwargs)

    def get_related_articles(self, limit=3):
        related = list(
            self.related_articles.filter(
                is_active=True,
                status=self.Status.PUBLISHED,
            ).exclude(pk=self.pk)[:limit]
        )
        if len(related) >= limit:
            return related

        needed = limit - len(related)
        exclude_ids = {self.pk, *[article.pk for article in related]}
        fallback = list(
            JournalArticle.objects.filter(
                is_active=True,
                status=self.Status.PUBLISHED,
                category_en=self.category_en,
            )
            .exclude(pk__in=exclude_ids)
            .order_by('-published_at')[:needed]
        )
        if len(fallback) < needed:
            exclude_ids.update(article.pk for article in fallback)
            fallback.extend(
                JournalArticle.objects.filter(
                    is_active=True,
                    status=self.Status.PUBLISHED,
                )
                .exclude(pk__in=exclude_ids)
                .order_by('-published_at')[: needed - len(fallback)]
            )
        return related + fallback



class Partner(SoftDeleteModel):
    name = models.CharField(max_length=255)
    logo_path = models.CharField(
        max_length=255,
        help_text='Static file path, e.g. images/partners/logo.png',
    )
    website_url = models.URLField(max_length=500, blank=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class GolfEvent(SoftDeleteModel):
    class Recurrence(models.TextChoices):
        NONE = 'none', 'One-time event'
        WEEKLY = 'weekly', 'Weekly'

    class Weekday(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    title_en = models.CharField(max_length=255)
    title_de = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='golf_events',
        db_index=True,
    )
    golf_course = models.ForeignKey(
        GolfCourse,
        on_delete=models.SET_NULL,
        related_name='events',
        db_index=True,
        blank=True,
        null=True,
    )
    summary_en = models.TextField(
        blank=True,
        help_text='Short excerpt shown on cards and under the hero.',
    )
    summary_de = models.TextField(blank=True)
    description_en = models.TextField(
        blank=True,
        help_text='Full event overview. Plain text; use blank lines between paragraphs.',
    )
    description_de = models.TextField(blank=True)
    format_label = models.CharField(
        max_length=120,
        blank=True,
        help_text='e.g. Members Guest Day, Invitational, Charity Pro-Am',
    )
    duration_label = models.CharField(
        max_length=120,
        blank=True,
        help_text='e.g. Morning round · about 5 hours',
    )
    dress_code = models.CharField(max_length=255, blank=True)
    eligibility_notes = models.TextField(
        blank=True,
        help_text='Handicap, membership, or guest requirements.',
    )
    inclusions = models.TextField(
        blank=True,
        help_text='One included item per line.',
    )
    need_to_know = models.TextField(
        blank=True,
        help_text='One preparation note per line.',
    )
    venue_notes = models.TextField(
        blank=True,
        help_text='Meeting point, clubhouse access, transfer notes.',
    )
    event_date = models.DateField(db_index=True)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)
    recurrence = models.CharField(
        max_length=20,
        choices=Recurrence.choices,
        default=Recurrence.NONE,
        db_index=True,
    )
    recurrence_weekday = models.PositiveSmallIntegerField(
        choices=Weekday.choices,
        blank=True,
        null=True,
        db_index=True,
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text='Featured image for listing and detail pages.',
    )
    registration_url = models.URLField(max_length=500, blank=True)
    accepts_inquiries = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Enable only for events guests are allowed to inquire about.',
    )
    is_promoted = models.BooleanField(default=False, db_index=True)
    promotion_priority = models.PositiveSmallIntegerField(
        default=100,
        db_index=True,
        help_text='Lower numbers appear first among promoted events.',
    )
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        ordering = [
            '-is_promoted',
            'promotion_priority',
            'event_date',
            'start_time',
            'title_en',
        ]

    def __str__(self):
        return self.title_en

    @property
    def is_recurring(self):
        return self.recurrence != self.Recurrence.NONE

    def get_inclusions(self):
        return [line.strip() for line in self.inclusions.splitlines() if line.strip()]

    def get_need_to_know(self):
        return [line.strip() for line in self.need_to_know.splitlines() if line.strip()]


class BasePackage(SoftDeleteModel):
    class PackageType(models.TextChoices):
        SAFARI = 'safari', _('Safari Focused')
        GOLF = 'golf', _('Golf Focused')
        GOLF_SAFARI = 'golf_safari', _('Safari + Golf')

    title_en = models.CharField(max_length=255)
    title_de = models.CharField(max_length=255)
    summary_en = models.TextField(blank=True)
    summary_de = models.TextField(blank=True)
    inclusions_en = models.TextField(
        blank=True,
        help_text='One included item per line.',
    )
    inclusions_de = models.TextField(
        blank=True,
        help_text='One included item per line.',
    )
    exclusions_en = models.TextField(
        blank=True,
        help_text='One excluded item per line.',
    )
    exclusions_de = models.TextField(
        blank=True,
        help_text='One excluded item per line.',
    )
    package_type = models.CharField(
        max_length=32,
        choices=PackageType.choices,
        default=PackageType.GOLF_SAFARI,
        db_index=True,
        help_text='Guest-facing journey focus shown on cards and detail pages.',
    )
    duration_days = models.PositiveIntegerField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    card_image_url = models.URLField(max_length=500, blank=True)
    hero_image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['title_en']

    def __str__(self):
        return self.title_en

    def get_inclusions(self, language_code='en'):
        source = (
            self.inclusions_de
            if language_code == 'de' and self.inclusions_de
            else self.inclusions_en
        )
        return [item.strip() for item in source.splitlines() if item.strip()]

    def get_exclusions(self, language_code='en'):
        source = (
            self.exclusions_de
            if language_code == 'de' and self.exclusions_de
            else self.exclusions_en
        )
        return [item.strip() for item in source.splitlines() if item.strip()]


class PackagePricingSeason(TimeStampedModel):
    base_package = models.ForeignKey(
        BasePackage,
        on_delete=models.CASCADE,
        related_name='pricing_seasons',
        db_index=True,
    )
    season_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price_usd = models.PositiveIntegerField()

    class Meta:
        ordering = ['base_package__title_en', 'start_date']
        indexes = [
            models.Index(fields=['base_package', 'start_date', 'end_date']),
        ]

    def __str__(self):
        return f'{self.base_package} - {self.season_name}'


class PackagePromotion(TimeStampedModel):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage discount'
        FIXED = 'fixed', 'Fixed discount amount'

    package = models.ForeignKey(
        BasePackage,
        on_delete=models.CASCADE,
        related_name='promotions',
        db_index=True,
    )
    label = models.CharField(
        max_length=80,
        help_text='Promotional label shown on cards and detail pages (e.g. “Green Season Sale”).',
    )
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
        db_index=True,
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Percentage (e.g. 15) or fixed USD amount (e.g. 500).',
    )
    show_featured_badge = models.BooleanField(
        default=False,
        db_index=True,
        help_text=(
            'Prefer this offer in the homepage Special Offers section '
            '(placement only — not shown as a badge on cards).'
        ),
        verbose_name='Feature in Special Offers',
    )
    show_in_banner = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Also rotate this offer in the sitewide promotional banner.',
    )
    banner_title = models.CharField(
        max_length=160,
        blank=True,
        help_text='Optional banner title override. Defaults to the package title.',
    )
    banner_description = models.CharField(
        max_length=280,
        blank=True,
        help_text='Optional banner description override.',
    )
    banner_cta_text = models.CharField(
        max_length=80,
        blank=True,
        help_text='Optional banner CTA override. Defaults to “View Offer”.',
    )
    is_active = models.BooleanField(default=True, db_index=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['display_order', '-start_date', 'id']
        indexes = [
            models.Index(fields=['is_active', 'start_date', 'end_date']),
            models.Index(fields=['show_featured_badge', 'is_active']),
            models.Index(fields=['show_in_banner', 'is_active']),
        ]

    def __str__(self):
        return f'{self.label} — {self.package}'

    @classmethod
    def active_queryset(cls, at=None):
        from django.utils import timezone

        moment = at or timezone.now()
        return cls.objects.filter(
            is_active=True,
            start_date__lte=moment,
            end_date__gte=moment,
        ).order_by('display_order', '-start_date', 'id')

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        errors = {}
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            errors['end_date'] = 'End date must be after the start date.'
        if self.discount_value is not None and self.discount_value <= 0:
            errors['discount_value'] = 'Discount value must be greater than zero.'
        if (
            self.discount_type == self.DiscountType.PERCENTAGE
            and self.discount_value is not None
            and self.discount_value > 100
        ):
            errors['discount_value'] = 'Percentage discounts cannot exceed 100.'
        if errors:
            raise ValidationError(errors)

    def discount_display(self):
        from decimal import Decimal, ROUND_HALF_UP

        if self.discount_type == self.DiscountType.PERCENTAGE:
            value = self.discount_value.normalize()
            return f'{value}% off'
        amount = int(
            Decimal(self.discount_value).quantize(
                Decimal('1'),
                rounding=ROUND_HALF_UP,
            )
        )
        return f'${amount:,} off'


class PackageItineraryDay(TimeStampedModel):
    base_package = models.ForeignKey(
        BasePackage,
        on_delete=models.CASCADE,
        related_name='itinerary_days',
        db_index=True,
    )
    day_number = models.PositiveIntegerField(db_index=True)
    title_en = models.CharField(max_length=255)
    title_de = models.CharField(max_length=255)
    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.SET_NULL,
        related_name='itinerary_days',
        db_index=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['base_package__title_en', 'day_number']
        constraints = [
            models.UniqueConstraint(
                fields=['base_package', 'day_number'],
                name='unique_package_itinerary_day',
            ),
        ]

    def __str__(self):
        return f'{self.base_package} - Day {self.day_number}'


class DayActivity(TimeStampedModel):
    itinerary_day = models.ForeignKey(
        PackageItineraryDay,
        on_delete=models.CASCADE,
        related_name='activities',
        db_index=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        db_index=True,
        limit_choices_to={
            'app_label': 'destination_cms',
            'model__in': [
                'golfcourse',
                'safaridestination',
                'wellnessexperience',
            ],
        },
    )
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['itinerary_day__day_number', 'display_order']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['itinerary_day', 'display_order']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['itinerary_day', 'display_order'],
                name='unique_day_activity_display_order',
            ),
        ]

    def __str__(self):
        return f'{self.itinerary_day} activity #{self.display_order}'


class PromotionalBanner(TimeStampedModel):
    class PromotionType(models.TextChoices):
        EVENT = 'event', 'Event'
        DISCOUNT = 'discount', 'Discount'
        LIMITED_OFFER = 'limited_offer', 'Limited-time Offer'
        FEATURED_SAFARI = 'featured_safari', 'Featured Safari Package'
        ANNOUNCEMENT = 'announcement', 'Announcement'

    title = models.CharField(max_length=160)
    short_description = models.CharField(max_length=280)
    cta_text = models.CharField(max_length=80)
    cta_url = models.CharField(
        max_length=500,
        help_text=(
            'Prefer a package detail path (e.g. /journeys/your-package-slug/) '
            'over listing pages like /journeys/.'
        ),
    )
    background_image_url = models.URLField(max_length=500, blank=True)
    promotion_type = models.CharField(
        max_length=32,
        choices=PromotionType.choices,
        default=PromotionType.ANNOUNCEMENT,
        db_index=True,
    )
    is_active = models.BooleanField(default=True, db_index=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    is_dismissible = models.BooleanField(
        default=True,
        help_text='Allow visitors to hide this banner for the rest of their browsing session.',
    )
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text='Lower numbers appear first in the rotation.',
    )

    class Meta:
        ordering = ['display_order', '-start_date', 'id']
        indexes = [
            models.Index(fields=['is_active', 'start_date', 'end_date']),
        ]

    def __str__(self):
        return self.title

    @classmethod
    def active_queryset(cls, at=None):
        from django.utils import timezone

        moment = at or timezone.now()
        return cls.objects.filter(
            is_active=True,
            start_date__lte=moment,
            end_date__gte=moment,
        ).order_by('display_order', '-start_date', 'id')

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError(
                {'end_date': 'End date must be after the start date.'}
            )