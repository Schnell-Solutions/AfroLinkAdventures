from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import DetailView, ListView, TemplateView

from analytics.mixins import TrackPageViewMixin
from analytics.models import EngagementEvent

from .models import (
    Accommodation,
    BasePackage,
    GalleryImage,
    GolfCourse,
    GolfEvent,
    JournalArticle,
    Partner,
    Region,
    SafariDestination,
    WellnessExperience,
)
from .promotions import (
    active_promotions_prefetch,
    build_package_card,
    build_package_pricing,
    featured_special_offer_cards,
)


EXPERIENCE_DETAIL_URLS = {
    'golfcourse': 'destination_cms:course_detail',
    'safaridestination': 'destination_cms:safari_detail',
    'safariextension': 'destination_cms:safari_detail',
    'accommodation': 'destination_cms:accommodation_detail',
    'wellnessexperience': 'destination_cms:wellness_detail',
}


def related_experience_cards(obj):
    cards = []
    for link in obj.get_related_links():
        target = link.to_object
        if target is None:
            continue
        model_name = link.to_content_type.model
        url_name = EXPERIENCE_DETAIL_URLS.get(model_name)
        slug = getattr(target, 'slug', None)
        if not url_name or not slug:
            continue
        title = (
            getattr(target, 'name', None)
            or getattr(target, 'name_en', None)
            or str(target)
        )
        hero = ''
        if hasattr(target, 'get_hero_image_url'):
            hero = target.get_hero_image_url()
        cards.append(
            {
                'label': link.label,
                'title': title,
                'url': reverse(url_name, kwargs={'slug': slug}),
                'image_url': hero,
            }
        )
    return cards


def experience_detail_context(obj):
    return {
        'included_items': obj.get_included_items(),
        'optional_items': obj.get_optional_items(),
        'faqs': obj.faqs.all(),
        'related_cards': related_experience_cards(obj),
        'hero_image_url': obj.get_hero_image_url(),
    }


def get_upcoming_events_queryset():
    today = timezone.localdate()
    return (
        GolfEvent.objects.filter(is_active=True, region__is_active=True)
        .filter(
            Q(event_date__gte=today)
            | Q(recurrence=GolfEvent.Recurrence.WEEKLY)
        )
        .select_related('region', 'golf_course')
        .order_by(
            '-is_promoted',
            'promotion_priority',
            'event_date',
            'start_time',
            'title_en',
        )
    )


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_packages = BasePackage.objects.filter(
            is_active=True
        ).prefetch_related('pricing_seasons', active_promotions_prefetch())[:3]
        featured_regions = Region.objects.filter(
            is_active=True
        ).prefetch_related('gallery_images')[:4]
        upcoming_events = list(get_upcoming_events_queryset()[:4])
        promoted_event = next(
            (event for event in upcoming_events if event.is_promoted),
            None,
        )
        featured_events = [
            event for event in upcoming_events if event != promoted_event
        ][:3]

        context['featured_package_cards'] = [
            build_package_card(base_package)
            for base_package in featured_packages
        ]
        context['special_offer_cards'] = featured_special_offer_cards(limit=3)
        context['featured_regions'] = featured_regions
        context['promoted_event'] = promoted_event
        context['featured_events'] = featured_events
        context['partners'] = Partner.objects.filter(is_active=True)
        return context


class RegionListView(ListView):
    model = Region
    template_name = 'destination_cms/region_list.html'
    context_object_name = 'regions'

    def get_queryset(self):
        return Region.objects.filter(is_active=True).prefetch_related(
            'gallery_images',
            Prefetch(
                'golf_courses',
                queryset=GolfCourse.objects.filter(is_active=True),
            ),
            Prefetch(
                'safari_destinations',
                queryset=SafariDestination.objects.filter(is_active=True),
            ),
            Prefetch(
                'wellness_experiences',
                queryset=WellnessExperience.objects.filter(is_active=True),
            ),
        )


class RegionalHubView(TrackPageViewMixin, DetailView):
    model = Region
    template_name = 'destination_cms/region_hub.html'
    context_object_name = 'region'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.DESTINATION_VIEW
    analytics_object_type = EngagementEvent.ObjectType.REGION

    def get_queryset(self):
        return (
            Region.objects.filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    'golf_courses',
                    queryset=GolfCourse.objects.filter(is_active=True).prefetch_related(
                        'gallery_images'
                    ),
                ),
                Prefetch(
                    'safari_destinations',
                    queryset=SafariDestination.objects.filter(
                        is_active=True
                    ).prefetch_related('gallery_images'),
                ),
                Prefetch(
                    'accommodations',
                    queryset=Accommodation.objects.filter(
                        is_active=True
                    ).prefetch_related('gallery_images'),
                ),
                Prefetch(
                    'wellness_experiences',
                    queryset=WellnessExperience.objects.filter(
                        is_active=True
                    ).prefetch_related('gallery_images'),
                ),
                'gallery_images',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        golf_courses = self.object.golf_courses.all()

        context.update(
            {
                'golf_courses': golf_courses,
                'premier_course': golf_courses[0] if golf_courses else None,
                'safari_destinations': self.object.safari_destinations.all(),
                'safari_extensions': self.object.safari_destinations.all(),
                'accommodations': self.object.accommodations.all(),
                'wellness_experiences': self.object.wellness_experiences.all(),
                'hero_image': self.object.gallery_images.first(),
            }
        )
        return context


class CourseListView(ListView):
    model = GolfCourse
    template_name = 'destination_cms/course_list.html'
    context_object_name = 'courses'

    def get_filters(self):
        params = self.request.GET
        return {
            'q': params.get('q', '').strip(),
            'region': params.get('region', '').strip(),
            'style': params.get('style', '').strip(),
            'championship': params.get('championship', '').strip(),
        }

    def get_queryset(self):
        return (
            GolfCourse.objects.filter(is_active=True, region__is_active=True)
            .select_related('region')
            .prefetch_related('gallery_images')
            .order_by('region__name_en', 'name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = self.get_filters()
        courses = list(context['courses'])

        context.update(
            {
                'filters': filters,
                'result_count': len(courses),
                'course_styles': GolfCourse.CourseStyle.choices,
                'filter_regions': Region.objects.filter(
                    is_active=True,
                    golf_courses__is_active=True,
                ).distinct(),
            }
        )
        return context


class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'destination_cms/accommodation_list.html'
    context_object_name = 'accommodations'

    def get_queryset(self):
        return (
            Accommodation.objects.filter(is_active=True, region__is_active=True)
            .select_related('region')
            .prefetch_related('gallery_images')
            .order_by('region__name_en', 'name')
        )


class AccommodationDetailView(TrackPageViewMixin, DetailView):
    model = Accommodation
    template_name = 'destination_cms/accommodation_detail.html'
    context_object_name = 'accommodation'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.DESTINATION_VIEW
    analytics_object_type = EngagementEvent.ObjectType.ACCOMMODATION

    def get_queryset(self):
        return (
            Accommodation.objects.filter(
                is_active=True,
                region__is_active=True,
                slug__isnull=False,
            )
            .select_related('region')
            .prefetch_related('gallery_images', 'faqs', 'offer_items')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(experience_detail_context(self.object))
        return context


def published_journal_queryset():
    return JournalArticle.objects.filter(
        is_active=True,
        status=JournalArticle.Status.PUBLISHED,
    )


class JournalArticleListView(ListView):
    model = JournalArticle
    template_name = 'destination_cms/journal.html'
    context_object_name = 'articles'

    def get_filters(self):
        params = self.request.GET
        return {
            'q': params.get('q', '').strip(),
            'category': params.get('category', '').strip(),
            'sort': params.get('sort', '').strip(),
        }

    def get_queryset(self):
        return published_journal_queryset().order_by('-published_at', 'title_en')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = self.get_filters()
        articles = list(context['articles'])
        featured_article = next(
            (article for article in articles if article.is_featured),
            articles[0] if articles else None,
        )

        context.update(
            {
                'featured_article': featured_article,
                'article_cards': articles,
                'filters': filters,
                'result_count': len(articles),
                'filter_categories': (
                    published_journal_queryset()
                    .exclude(category_en='')
                    .values_list('category_en', flat=True)
                    .distinct()
                    .order_by('category_en')
                ),
            }
        )
        return context


class JournalArticleDetailView(TrackPageViewMixin, DetailView):
    model = JournalArticle
    template_name = 'destination_cms/journal_detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.JOURNAL_VIEW
    analytics_object_type = EngagementEvent.ObjectType.JOURNAL

    def get_queryset(self):
        return published_journal_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context['article']
        context['related_articles'] = article.get_related_articles(limit=3)
        return context


class CourseDetailView(TrackPageViewMixin, DetailView):
    model = GolfCourse
    template_name = 'destination_cms/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.DESTINATION_VIEW
    analytics_object_type = EngagementEvent.ObjectType.COURSE

    def get_queryset(self):
        return (
            GolfCourse.objects.filter(is_active=True, region__is_active=True)
            .select_related('region')
            .prefetch_related('gallery_images', 'faqs', 'offer_items')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(experience_detail_context(self.object))
        return context


class GolfEventListView(ListView):
    model = GolfEvent
    template_name = 'destination_cms/event_list.html'
    context_object_name = 'events'

    def get_filters(self):
        params = self.request.GET
        return {
            'q': params.get('q', '').strip(),
            'region': params.get('region', '').strip(),
            'type': params.get('type', '').strip(),
            'date_from': parse_date(params.get('date_from', '') or ''),
            'date_to': parse_date(params.get('date_to', '') or ''),
        }

    def get_queryset(self):
        return get_upcoming_events_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = self.get_filters()
        events = list(context['events'])
        promoted_events = [event for event in events if event.is_promoted]

        context.update(
            {
                'promoted_events': promoted_events,
                'regular_events': events,
                'filters': {
                    **filters,
                    'date_from': filters['date_from'],
                    'date_to': filters['date_to'],
                },
                'result_count': len(events),
                'filter_regions': Region.objects.filter(
                    is_active=True,
                    golf_events__is_active=True,
                ).distinct(),
            }
        )
        return context


class GolfEventDetailView(TrackPageViewMixin, DetailView):
    model = GolfEvent
    template_name = 'destination_cms/event_detail.html'
    context_object_name = 'event'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.EVENT_VIEW
    analytics_object_type = EngagementEvent.ObjectType.EVENT

    def get_queryset(self):
        return (
            GolfEvent.objects.filter(
                is_active=True,
                region__is_active=True,
            )
            .select_related('region', 'golf_course')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context['event']
        related_events = list(
            get_upcoming_events_queryset()
            .filter(region=event.region)
            .exclude(pk=event.pk)
            .select_related('region', 'golf_course')[:3]
        )
        if len(related_events) < 3:
            exclude_ids = {event.pk, *[item.pk for item in related_events]}
            related_events.extend(
                get_upcoming_events_queryset()
                .exclude(pk__in=exclude_ids)
                .select_related('region', 'golf_course')[: 3 - len(related_events)]
            )
        context['related_events'] = related_events
        return context


class SafariListView(ListView):
    model = SafariDestination
    template_name = 'destination_cms/safari_list.html'
    context_object_name = 'safari_extensions'

    def get_filters(self):
        params = self.request.GET
        return {
            'q': params.get('q', '').strip(),
            'region': params.get('region', '').strip(),
            'big_five': params.get('big_five', '').strip(),
            'experience': params.get('experience', '').strip(),
        }

    def get_queryset(self):
        return (
            SafariDestination.objects.filter(is_active=True, region__is_active=True)
            .select_related('region')
            .prefetch_related('gallery_images')
            .order_by('region__name_en', 'name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        safaris = list(context['safari_extensions'])
        context.update(
            {
                'filters': self.get_filters(),
                'result_count': len(safaris),
                'filter_regions': Region.objects.filter(
                    is_active=True,
                    safari_destinations__is_active=True,
                ).distinct(),
            }
        )
        return context


class SafariDetailView(TrackPageViewMixin, DetailView):
    model = SafariDestination
    template_name = 'destination_cms/safari_detail.html'
    context_object_name = 'safari'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.DESTINATION_VIEW
    analytics_object_type = EngagementEvent.ObjectType.SAFARI

    def get_queryset(self):
        return (
            SafariDestination.objects.filter(
                is_active=True,
                region__is_active=True,
                slug__isnull=False,
            )
            .select_related('region')
            .prefetch_related(
                'gallery_images',
                'faqs',
                'offer_items',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(experience_detail_context(self.object))
        return context


class WellnessDetailView(TrackPageViewMixin, DetailView):
    model = WellnessExperience
    template_name = 'destination_cms/wellness_detail.html'
    context_object_name = 'wellness'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.DESTINATION_VIEW
    analytics_object_type = EngagementEvent.ObjectType.WELLNESS

    def get_queryset(self):
        return (
            WellnessExperience.objects.filter(
                is_active=True,
                region__is_active=True,
                slug__isnull=False,
            )
            .select_related('region')
            .prefetch_related('gallery_images', 'faqs', 'offer_items')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(experience_detail_context(self.object))
        return context


class PackageListView(ListView):
    model = BasePackage
    template_name = 'destination_cms/package_list.html'
    context_object_name = 'packages'

    def get_filters(self):
        params = self.request.GET
        return {
            'q': params.get('q', '').strip(),
            'type': params.get('type', '').strip(),
            'duration': params.get('duration', '').strip(),
            'offer': params.get('offer', '').strip(),
            'sort': params.get('sort', '').strip(),
        }

    def get_queryset(self):
        return (
            BasePackage.objects.filter(is_active=True)
            .prefetch_related('pricing_seasons', active_promotions_prefetch())
            .order_by('title_en')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = self.get_filters()
        cards = [
            build_package_card(base_package)
            for base_package in context['packages']
        ]

        context.update(
            {
                'package_cards': cards,
                'filters': filters,
                'result_count': len(cards),
            }
        )
        return context


class PackageDetailView(TrackPageViewMixin, DetailView):
    model = BasePackage
    template_name = 'destination_cms/package_detail.html'
    context_object_name = 'package'
    slug_url_kwarg = 'slug'
    analytics_event_type = EngagementEvent.EventType.PACKAGE_VIEW
    analytics_object_type = EngagementEvent.ObjectType.PACKAGE

    def get_queryset(self):
        return (
            BasePackage.objects.filter(is_active=True)
            .prefetch_related(
                'pricing_seasons',
                active_promotions_prefetch(),
                'itinerary_days__accommodation',
                'itinerary_days__activities__content_type',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pricing = build_package_pricing(self.object)
        package_content_type = ContentType.objects.get_for_model(self.object)
        gallery_hero_image = GalleryImage.objects.filter(
            content_type=package_content_type,
            object_id=self.object.pk,
        ).first()
        hero_image_url = self.object.hero_image_url or (
            gallery_hero_image.image_url if gallery_hero_image else ''
        )
        package_description = (
            self.object.summary_de
            if self.request.LANGUAGE_CODE == 'de' and self.object.summary_de
            else self.object.summary_en
        )

        context.update(
            {
                **pricing,
                'itinerary_days': self.object.itinerary_days.all(),
                'hero_image_url': hero_image_url,
                'included_items': self.object.get_inclusions(
                    self.request.LANGUAGE_CODE
                ),
                'excluded_items': self.object.get_exclusions(
                    self.request.LANGUAGE_CODE
                ),
                'package_description': package_description or (
                    'A private AfroLink journey shaped around championship '
                    'golf, safari access, regional transfers, and unhurried '
                    'recovery time between signature experiences.'
                ),
            }
        )
        return context
