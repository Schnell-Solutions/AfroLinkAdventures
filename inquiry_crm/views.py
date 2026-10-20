from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Q
from django.core.signing import BadSignature, SignatureExpired
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.html import format_html, strip_tags
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView

from analytics.mixins import TrackPageViewMixin
from analytics.models import EngagementEvent
from analytics.services import track
from destination_cms.models import (
    Accommodation,
    BasePackage,
    GolfCourse,
    GolfEvent,
    Region,
    SafariDestination,
    WellnessExperience,
)
from destination_cms.promotions import (
    active_promotions_prefetch,
    build_package_card,
    build_package_pricing,
)

from .models import (
    Consultation,
    ExperienceInquiry,
    Inquiry,
    InquiryCustomDay,
    InquiryInterest,
    InquiryPackage,
    Lead,
)
from .tokens import (
    earliest_allowed_consultation_date,
    preferred_window_to_datetime,
    sign_inquiry_confirmation,
    unsign_inquiry_confirmation,
)


INQUIRY_LIGHT_INTENTS = frozenset({'consultation', 'direct', 'light'})


INTEREST_CONFIG = {
    InquiryInterest.InterestType.GOLF_COURSE: {
        'model': GolfCourse,
        'title_attr': 'name',
        'message_label': 'Golf course',
    },
    InquiryInterest.InterestType.SAFARI_EXTENSION: {
        'model': SafariDestination,
        'title_attr': 'name',
        'message_label': 'Safari destination',
    },
    InquiryInterest.InterestType.ACCOMMODATION: {
        'model': Accommodation,
        'title_attr': 'name',
        'message_label': 'Stay',
    },
    InquiryInterest.InterestType.WELLNESS_EXPERIENCE: {
        'model': WellnessExperience,
        'title_attr': 'name_en',
        'message_label': 'Wellness experience',
    },
    InquiryInterest.InterestType.GOLF_EVENT: {
        'model': GolfEvent,
        'title_attr': 'title_en',
        'message_label': 'Golf event',
        'requires_accepts_inquiries': True,
    },
}


class PackageListView(ListView):
    model = BasePackage
    template_name = 'inquiry_crm/package_list.html'
    context_object_name = 'packages'

    def get_queryset(self):
        return BasePackage.objects.filter(is_active=True).prefetch_related(
            'pricing_seasons',
            active_promotions_prefetch(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_cards = []

        for base_package in context['packages']:
            card = build_package_card(base_package)
            if card['starting_price'] is not None:
                suffix = ' per person sharing'
                card['starting_price_label'] = f"{card['starting_price_label']}{suffix}"
                if card['has_promo_price']:
                    card['original_price_label'] = (
                        f"{card['original_price_label']}{suffix}"
                    )
                    card['promo_price_label'] = (
                        f"{card['promo_price_label']}{suffix}"
                    )
            package_cards.append(card)

        context['package_cards'] = package_cards
        return context


def parse_positive_integer(value, field_name, minimum=1, maximum=60):
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f'{field_name} must be a whole number.') from exc

    if parsed < minimum or parsed > maximum:
        raise ValidationError(
            f'{field_name} must be between {minimum} and {maximum}.'
        )

    return parsed


def parse_scheduled_time(value):
    parsed = parse_datetime(value or '')
    if parsed is None:
        raise ValidationError('Please select a valid consultation time.')

    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())

    return parsed


def add_package_to_session_cart(request, base_package):
    """Keep nav/dock counts in sync when a signature journey is selected."""
    inquiry_cart = list(request.session.get('inquiry_cart', []))
    already_added = any(
        item.get('item_type') == 'package'
        and str(item.get('package_id')) == str(base_package.id)
        for item in inquiry_cart
    )
    if already_added:
        return False

    inquiry_cart.append(
        {
            'item_type': 'package',
            'package_id': base_package.id,
            'title': base_package.title_en,
        }
    )
    request.session['inquiry_cart'] = inquiry_cart
    request.session.modified = True
    return True


def send_inquiry_mail(*, subject, message, recipient_list):
    """Send mail with visible failures in DEBUG; quiet in production."""
    if not recipient_list:
        return False
    fail_silently = not settings.DEBUG
    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(recipient_list),
            fail_silently=fail_silently,
        )
        return bool(sent)
    except Exception:
        if settings.DEBUG:
            raise
        return False


class PackageDetailView(TrackPageViewMixin, DetailView):
    model = BasePackage
    template_name = 'inquiry_crm/itinerary_detail.html'
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
        suffix = ' per person sharing'
        if pricing['starting_price'] is not None:
            pricing['starting_price_label'] = (
                f"{pricing['starting_price_label']}{suffix}"
            )
            if pricing['has_promo_price']:
                pricing['original_price_label'] = (
                    f"{pricing['original_price_label']}{suffix}"
                )
                pricing['promo_price_label'] = (
                    f"{pricing['promo_price_label']}{suffix}"
                )
        context.update(pricing)
        context['itinerary_days'] = self.object.itinerary_days.all()
        return context


@require_POST
def add_to_inquiry_list(request, slug):
    base_package = get_object_or_404(BasePackage, slug=slug, is_active=True)
    add_package_to_session_cart(request, base_package)
    return redirect(
        f"{reverse('inquiry_crm:inquiry_intake')}?package={base_package.slug}"
    )


def package_enquiry(request, slug):
    base_package = get_object_or_404(BasePackage, slug=slug, is_active=True)
    add_package_to_session_cart(request, base_package)
    return redirect(
        f"{reverse('inquiry_crm:inquiry_intake')}?package={base_package.slug}"
    )


@require_POST
def add_interest_to_inquiry_list(request):
    interest_type = request.POST.get('interest_type')
    object_id = request.POST.get('object_id')
    redirect_url = request.POST.get('next') or request.META.get(
        'HTTP_REFERER',
        reverse('inquiry_crm:start_inquiry'),
    )
    config = INTEREST_CONFIG.get(interest_type)

    if not config:
        messages.error(request, _('Unable to add this item to your shortlist.'))
        return redirect(redirect_url)

    content_object = get_object_or_404(
        config['model'],
        id=object_id,
        is_active=True,
    )
    if config.get('requires_accepts_inquiries') and not getattr(
        content_object,
        'accepts_inquiries',
        False,
    ):
        messages.error(
            request,
            _('This event is not currently open for direct inquiries.'),
        )
        return redirect(redirect_url)

    content_type = ContentType.objects.get_for_model(
        content_object,
        for_concrete_model=False,
    )
    title = getattr(content_object, config['title_attr'])
    inquiry_cart = request.session.get('inquiry_cart', [])
    already_added = any(
        item.get('item_type') == interest_type
        and str(item.get('object_id')) == str(content_object.id)
        for item in inquiry_cart
    )

    if not already_added:
        inquiry_cart.append(
            {
                'item_type': interest_type,
                'content_type_id': content_type.id,
                'object_id': content_object.id,
                'title': title,
            }
        )
        request.session['inquiry_cart'] = inquiry_cart
        request.session.modified = True

    custom_package_url = reverse('inquiry_crm:custom_package')
    messages.success(
        request,
        format_html(
            '<div class="toast__body">'
            '<p>{}</p>'
            '<div class="toast__actions">'
            '<a class="toast__action" href="{}">{}</a>'
            '</div>'
            '<p class="inquiry-commitment inquiry-commitment--compact">{}</p>'
            '</div>',
            _('%(label)s added to your shortlist.')
            % {'label': config['message_label']},
            custom_package_url,
            _('Complete enquiry'),
            _(
                'Nothing is booked until you have had a video consultation '
                'and the plan is confirmed.'
            ),
        ),
        extra_tags='toast-rich',
    )
    return redirect(redirect_url)


@require_POST
def remove_from_inquiry_list(request):
    # The remove buttons submit the intake form via formaction, carrying the
    # target as a single "item_type:object_id" value.
    item_type, _, object_id = request.POST.get('remove_item', '').partition(':')
    inquiry_cart = request.session.get('inquiry_cart', [])

    if item_type == 'package':
        updated_cart = [
            item
            for item in inquiry_cart
            if not (
                item.get('item_type') == 'package'
                and str(item.get('package_id')) == object_id
            )
        ]
    else:
        updated_cart = [
            item
            for item in inquiry_cart
            if not (
                item.get('item_type') == item_type
                and str(item.get('object_id')) == object_id
            )
        ]

    removed = len(updated_cart) != len(inquiry_cart)
    success_message = _('Item removed from your shortlist.')

    if removed:
        request.session['inquiry_cart'] = updated_cart
        request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(
            {
                'success': removed,
                'message': (
                    success_message
                    if removed
                    else _('Item could not be removed.')
                ),
                'cart_count': len(updated_cart),
            }
        )

    if removed:
        messages.success(request, success_message)

    redirect_url = request.POST.get('next') or reverse(
        'inquiry_crm:custom_package'
    )
    return redirect(redirect_url)


class CustomPlannerView(TemplateView):
    template_name = 'inquiry_crm/custom_planner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'regions': Region.objects.filter(is_active=True),
                'golf_courses': GolfCourse.objects.filter(
                    is_active=True,
                    region__is_active=True,
                ).select_related('region'),
                'safari_extensions': SafariDestination.objects.filter(
                    is_active=True,
                    region__is_active=True,
                ).select_related('region'),
            }
        )
        return context


class InquiryStartView(TemplateView):
    """Light entry chooser before planner or intake."""

    template_name = 'inquiry_crm/inquiry_start.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('inquiry_cart'):
            return redirect(reverse('inquiry_crm:custom_package'))
        return super().get(request, *args, **kwargs)


class InquiryIntakeView(View):
    template_name = 'inquiry_crm/inquiry_intake.html'

    def get(self, request):
        if self.should_redirect_empty_start(request):
            return redirect(reverse('inquiry_crm:inquiry_start'))

        context = self.get_selection_context(request.GET, request)
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.get_selection_context(request.POST, request)
        errors = []

        try:
            target_start_date = self.parse_optional_date(
                request.POST.get('target_start_date')
            )
            guest_count = parse_positive_integer(
                request.POST.get('guest_count'),
                'Guest quantity',
                minimum=1,
                maximum=12,
            )
            day_count = parse_positive_integer(
                request.POST.get('day_count') or '1',
                'Number of days',
                minimum=1,
                maximum=60,
            )
        except ValidationError as exc:
            errors.extend(exc.messages)
            target_start_date = None
            guest_count = None
            day_count = None

        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()[:40]
        preferred_language = request.POST.get(
            'preferred_language',
            Lead.PreferredLanguage.ENGLISH,
        )
        preferred_contact = request.POST.get(
            'preferred_contact',
            Lead.PreferredContact.EMAIL,
        )
        budget_band = (request.POST.get('budget_band') or '').strip()
        trip_flexibility = (request.POST.get('trip_flexibility') or '').strip()
        luggage_acknowledged = (
            request.POST.get('luggage_limit_acknowledged') == 'on'
        )
        accommodation_tier = request.POST.get(
            'accommodation_tier',
            Inquiry.AccommodationTier.STANDARD_LUXURY,
        )
        preferred_consultation_date_raw = (
            request.POST.get('preferred_consultation_date') or ''
        ).strip()
        preferred_consultation_window = (
            request.POST.get('preferred_consultation_window') or ''
        ).strip()
        additional_requirements = (
            request.POST.get('additional_requirements') or ''
        ).strip()
        if len(additional_requirements) > 4000:
            errors.append(
                'Please keep additional requirements under 4000 characters.'
            )

        if not full_name:
            errors.append('Full name is required.')
        if not email:
            errors.append('Email is required.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Please enter a valid email address.')
        if preferred_language not in Lead.PreferredLanguage.values:
            errors.append('Preferred language must be English or Deutsch.')
        if preferred_contact not in Lead.PreferredContact.values:
            errors.append('Please select a preferred contact method.')
        if budget_band and budget_band not in Lead.BudgetBand.values:
            errors.append('Please select a valid budget band.')
        if (
            trip_flexibility
            and trip_flexibility not in Lead.TripFlexibility.values
        ):
            errors.append('Please select a valid trip flexibility option.')
        if accommodation_tier not in Inquiry.AccommodationTier.values:
            errors.append('Please select a valid accommodation preference.')
        if not luggage_acknowledged:
            errors.append('Please acknowledge the 22kg golf bag limit.')

        preferred_consultation_date = None
        scheduled_time = None
        if not preferred_consultation_date_raw:
            errors.append('Please choose a preferred consultation date.')
        else:
            preferred_consultation_date = parse_date(
                preferred_consultation_date_raw
            )
            if preferred_consultation_date is None:
                errors.append('Please select a valid consultation date.')
            elif preferred_consultation_date < earliest_allowed_consultation_date():
                errors.append(
                    'Consultation date must be tomorrow or later (East Africa Time).'
                )

        if (
            preferred_consultation_window
            not in Inquiry.PreferredWindow.values
        ):
            errors.append('Please select a preferred consultation window.')
        elif preferred_consultation_date is not None:
            scheduled_time = preferred_window_to_datetime(
                preferred_consultation_date,
                preferred_consultation_window,
            )

        package_ids = request.POST.getlist('package_ids')
        selected_package_ids = request.POST.getlist('selected_package_ids')
        package_ids = package_ids or selected_package_ids
        golf_course_ids = [
            value for value in request.POST.getlist('golf_course_ids') if value
        ]
        safari_extension_ids = [
            value
            for value in request.POST.getlist('safari_extension_ids')
            if value
        ]
        region_id = request.POST.get('region_id')
        planning_focus = request.POST.get('planning_focus', '').strip()
        travel_pace = request.POST.get('travel_pace', '').strip()
        accommodation_style = request.POST.get('accommodation_style', '').strip()
        interest_items = self.get_interest_items_from_payload(request.POST)
        if not interest_items:
            interest_items = self.get_session_interest_items(request)

        intent = request.POST.get('intent') or request.GET.get('intent') or ''
        has_substance = bool(
            package_ids
            or interest_items
            or golf_course_ids
            or safari_extension_ids
            or intent in INQUIRY_LIGHT_INTENTS
            or planning_focus
            or region_id
        )
        if not has_substance:
            errors.append(
                'Please select a journey, build a shortlist, or start from '
                'Request a consultation.'
            )

        if errors:
            context.update(
                {
                    'errors': errors,
                    'form_values': request.POST,
                }
            )
            return render(request, self.template_name, context, status=400)

        with transaction.atomic():
            lead = Lead.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                preferred_language=preferred_language,
                preferred_contact=preferred_contact,
                budget_band=budget_band,
                trip_flexibility=trip_flexibility,
                inquiry_status=Lead.InquiryStatus.CONSULTATION,
                planning_focus=planning_focus[:120],
                travel_pace=travel_pace[:120],
                accommodation_style=accommodation_style[:120],
                notes=self.build_lead_notes(
                    planning_focus,
                    travel_pace,
                    accommodation_style,
                ),
            )
            inquiry = Inquiry.objects.create(
                lead=lead,
                inquiry_type=self.resolve_inquiry_type(
                    package_ids,
                    golf_course_ids,
                    safari_extension_ids,
                    interest_items,
                ),
                status=Lead.InquiryStatus.CONSULTATION,
                target_start_date=target_start_date,
                guest_count=guest_count,
                accommodation_tier=accommodation_tier,
                preferred_consultation_date=preferred_consultation_date,
                preferred_consultation_window=preferred_consultation_window,
                luggage_limit_acknowledged=luggage_acknowledged,
                additional_requirements=additional_requirements,
            )

            packages = BasePackage.objects.filter(
                id__in=package_ids,
                is_active=True,
            )
            for base_package in packages:
                InquiryPackage.objects.create(
                    inquiry=inquiry,
                    base_package=base_package,
                    notes='Selected as the primary package enquiry.',
                )

            self.create_inquiry_interests(inquiry, interest_items)

            if region_id and (golf_course_ids or safari_extension_ids):
                self.create_custom_days(
                    inquiry=inquiry,
                    region_id=region_id,
                    golf_course_ids=golf_course_ids,
                    safari_extension_ids=safari_extension_ids,
                    day_count=day_count,
                )

            Consultation.objects.create(
                inquiry=inquiry,
                scheduled_time=scheduled_time,
                meeting_url='',
            )

        request.session['inquiry_cart'] = []
        request.session.modified = True

        track(
            event_type=EngagementEvent.EventType.INQUIRY_SUBMIT,
            object_type=EngagementEvent.ObjectType.INQUIRY,
            object_id=inquiry.id,
            object_label=f'Inquiry #{inquiry.id}',
            metadata={
                'inquiry_type': inquiry.inquiry_type,
                'package_count': len(package_ids),
                'interest_count': len(interest_items),
            },
            request=request,
        )

        _notify_inquiry_submitted(inquiry)

        return redirect(
            reverse(
                'inquiry_crm:inquiry_confirmation',
                kwargs={'token': sign_inquiry_confirmation(inquiry.id)},
            )
        )

    def should_redirect_empty_start(self, request):
        if request.GET.get('intent') in INQUIRY_LIGHT_INTENTS:
            return False
        has_package = bool(
            request.GET.getlist('package') or request.GET.getlist('package_ids')
        )
        has_custom_cart = bool(request.session.get('inquiry_cart', []))
        has_planner_payload = any(
            request.GET.get(key)
            for key in (
                'region_id',
                'planning_focus',
                'travel_pace',
                'accommodation_style',
            )
        )
        return not has_package and not has_custom_cart and not has_planner_payload

    def parse_optional_date(self, value):
        if not value:
            return None

        parsed = parse_date(value)
        if parsed is None:
            raise ValidationError('Please select a valid target start date.')

        return parsed

    def get_selection_context(self, payload, request=None):
        package_slugs = payload.getlist('package')
        package_ids = payload.getlist('package_ids')
        session_package_ids = (
            self.get_session_package_ids(request)
            if request is not None
            else []
        )
        package_ids = list(dict.fromkeys([*package_ids, *session_package_ids]))
        package_filter = Q()
        if package_slugs:
            package_filter |= Q(slug__in=package_slugs)
        if package_ids:
            package_filter |= Q(id__in=package_ids)

        packages = (
            BasePackage.objects.filter(package_filter, is_active=True)
            if package_filter
            else BasePackage.objects.filter(is_active=True).none()
        )

        region_id = payload.get('region_id')
        selected_region = None
        if region_id:
            selected_region = Region.objects.filter(
                id=region_id,
                is_active=True,
            ).first()

        selected_interests = (
            self.get_session_interest_items(request)
            if request is not None
            else []
        )
        payload_interests = self.get_interest_items_from_payload(payload)
        if payload_interests:
            selected_interests = payload_interests

        return {
            'selected_packages': packages,
            'selected_interests': selected_interests,
            'selected_region': selected_region,
            'has_package_enquiry': packages.exists(),
            'has_custom_package': bool(selected_interests),
            'inquiry_flow': (
                'package' if packages.exists() else 'custom'
            ),
            'inquiry_step': 'details',
            'has_planner_brief': bool(
                selected_region
                or payload.get('planning_focus')
                or payload.get('travel_pace')
                or payload.get('accommodation_style')
            ),
            'day_count': payload.get('day_count', '7'),
            'golf_course_ids': [
                value for value in payload.getlist('golf_course_ids') if value
            ],
            'safari_extension_ids': [
                value
                for value in payload.getlist('safari_extension_ids')
                if value
            ],
            'planning_focus': payload.get('planning_focus', ''),
            'travel_pace': payload.get('travel_pace', ''),
            'accommodation_style': payload.get('accommodation_style', ''),
            'form_values': payload,
            'errors': [],
            'budget_band_choices': Lead.BudgetBand.choices,
            'trip_flexibility_choices': Lead.TripFlexibility.choices,
            'preferred_contact_choices': Lead.PreferredContact.choices,
            'consultation_window_choices': Inquiry.PreferredWindow.choices,
            'min_consultation_date': earliest_allowed_consultation_date().isoformat(),
            'intent': payload.get('intent', ''),
        }

    def get_session_package_ids(self, request):
        if request is None:
            return []

        return [
            str(item.get('package_id'))
            for item in request.session.get('inquiry_cart', [])
            if item.get('package_id')
        ]

    def get_session_interest_items(self, request):
        if request is None:
            return []

        return [
            {
                'interest_type': item.get('item_type'),
                'content_type_id': item.get('content_type_id'),
                'object_id': item.get('object_id'),
                'title': item.get('title'),
            }
            for item in request.session.get('inquiry_cart', [])
            if item.get('content_type_id') and item.get('object_id')
        ]

    def get_interest_items_from_payload(self, payload):
        interest_types = payload.getlist('interest_type')
        content_type_ids = payload.getlist('interest_content_type_id')
        object_ids = payload.getlist('interest_object_id')
        titles = payload.getlist('interest_title')
        interests = []

        for index, interest_type in enumerate(interest_types):
            try:
                content_type_id = content_type_ids[index]
                object_id = object_ids[index]
                title = titles[index]
            except IndexError:
                continue

            if interest_type and content_type_id and object_id and title:
                interests.append(
                    {
                        'interest_type': interest_type,
                        'content_type_id': content_type_id,
                        'object_id': object_id,
                        'title': title,
                    }
                )

        return interests

    def build_lead_notes(
        self,
        planning_focus,
        travel_pace,
        accommodation_style,
    ):
        notes = ['Submitted through the concierge portfolio workflow.']

        if accommodation_style:
            notes.append(f'Accommodation preference: {accommodation_style}.')
        if planning_focus:
            notes.append(f'Planning focus: {planning_focus}.')
        if travel_pace:
            notes.append(f'Travel pace: {travel_pace}.')

        return '\n'.join(notes)

    def create_inquiry_interests(self, inquiry, interest_items):
        for item in interest_items:
            if item['interest_type'] not in InquiryInterest.InterestType.values:
                continue

            InquiryInterest.objects.get_or_create(
                inquiry=inquiry,
                content_type_id=item['content_type_id'],
                object_id=item['object_id'],
                defaults={
                    'interest_type': item['interest_type'],
                    'title_snapshot': item['title'],
                    'notes': 'Added from the session inquiry portfolio.',
                },
            )

    def resolve_inquiry_type(
        self,
        package_ids,
        golf_course_ids,
        safari_ids,
        interest_items=None,
    ):
        has_packages = bool(package_ids)
        has_custom = bool(golf_course_ids or safari_ids or interest_items)

        if has_packages and has_custom:
            return Inquiry.InquiryType.MIXED
        if has_packages:
            return Inquiry.InquiryType.PRE_SET_PACKAGES
        return Inquiry.InquiryType.CUSTOM_BUILD

    def create_custom_days(
        self,
        inquiry,
        region_id,
        golf_course_ids,
        safari_extension_ids,
        day_count,
    ):
        region = get_object_or_404(Region, id=region_id, is_active=True)
        golf_courses = list(
            GolfCourse.objects.filter(
                id__in=golf_course_ids,
                region=region,
                is_active=True,
            )
        )
        safari_extensions = list(
            SafariDestination.objects.filter(
                id__in=safari_extension_ids,
                region=region,
                is_active=True,
            )
        )

        for day_index in range(day_count):
            InquiryCustomDay.objects.create(
                inquiry=inquiry,
                day_number=day_index + 1,
                region=region,
                golf_course=(
                    golf_courses[day_index]
                    if day_index < len(golf_courses)
                    else None
                ),
                safari_extension=(
                    safari_extensions[day_index]
                    if day_index < len(safari_extensions)
                    else None
                ),
            )


class InquiryConfirmationView(DetailView):
    model = Inquiry
    template_name = 'inquiry_crm/inquiry_confirmation.html'
    context_object_name = 'inquiry'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token', '')
        try:
            inquiry_id = unsign_inquiry_confirmation(token)
        except (BadSignature, SignatureExpired, ValueError, TypeError) as exc:
            raise Http404('Enquiry confirmation link is invalid or expired.') from exc

        queryset = self.get_queryset() if queryset is None else queryset
        return get_object_or_404(queryset, pk=inquiry_id)

    def get_queryset(self):
        return (
            Inquiry.objects.select_related('lead')
            .prefetch_related(
                'package_shortlist__base_package',
                'custom_days__region',
                'custom_days__golf_course',
                'custom_days__safari_extension',
                'interests',
                'consultations',
            )
        )


def _inquiry_notify_recipients():
    recipients = getattr(settings, 'INQUIRY_NOTIFY_EMAILS', None) or []
    if not recipients:
        default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        if default_from:
            # Extract bare email if "Name <email>" form
            if '<' in default_from and '>' in default_from:
                recipients = [default_from.split('<')[1].rstrip('>').strip()]
            else:
                recipients = [default_from]
    return list(recipients)


def _notify_inquiry_submitted(inquiry):
    """Staff alert + guest acknowledgement after a full CRM enquiry submit."""
    lead = inquiry.lead
    interests = list(inquiry.interests.all())
    packages = list(inquiry.package_shortlist.select_related('base_package'))
    consultations = list(inquiry.consultations.all())

    interest_lines = ', '.join(item.title_snapshot for item in interests) or 'None'
    package_lines = (
        ', '.join(link.base_package.title_en for link in packages) or 'None'
    )
    preferred_window = (
        consultations[0].scheduled_time.strftime('%Y-%m-%d %H:%M %Z')
        if consultations
        else 'Not specified'
    )
    if inquiry.preferred_consultation_window:
        preferred_window = (
            f'{inquiry.preferred_consultation_date} · '
            f'{inquiry.get_preferred_consultation_window_display()} '
            f'(stored as {preferred_window})'
        )
    extra = inquiry.additional_requirements or 'None provided'

    staff_recipients = _inquiry_notify_recipients()
    if staff_recipients:
        staff_subject = f'[AfroLink] New enquiry #{inquiry.id} from {lead.full_name}'
        staff_body = (
            f'A guest submitted a concierge enquiry.\n\n'
            f'Inquiry ID: {inquiry.id}\n'
            f'Name: {lead.full_name}\n'
            f'Email: {lead.email}\n'
            f'Phone: {lead.phone or "Not provided"}\n'
            f'Preferred contact: {lead.get_preferred_contact_display()}\n'
            f'Language: {lead.get_preferred_language_display()}\n'
            f'Budget: {lead.get_budget_band_display() or "Not provided"}\n'
            f'Trip flexibility: {lead.get_trip_flexibility_display() or "Not provided"}\n'
            f'Type: {inquiry.get_inquiry_type_display()}\n'
            f'Guests: {inquiry.guest_count}\n'
            f'Target start: {inquiry.target_start_date or "Flexible"}\n'
            f'Accommodation: {inquiry.get_accommodation_tier_display()}\n'
            f'Preferred consultation window: {preferred_window}\n'
            f'Packages: {package_lines}\n'
            f'Shortlist: {interest_lines}\n\n'
            f'Additional requirements:\n{extra}\n'
        )
        send_inquiry_mail(
            subject=staff_subject,
            message=staff_body,
            recipient_list=staff_recipients,
        )

    if lead.email:
        guest_subject = 'We received your AfroLink enquiry'
        guest_body = (
            f'Dear {lead.full_name},\n\n'
            f'Thank you for your enquiry with AfroLink Adventures. '
            f'We have received your request and nothing is booked yet.\n\n'
            f'Within two hours we will email you with a proposed video '
            f'consultation time and joining details.\n\n'
            f'Enquiry reference: #{inquiry.id}\n'
            f'Type: {inquiry.get_inquiry_type_display()}\n'
            f'Preferred consultation window: {preferred_window}\n\n'
            f'On the call we will refine dates, routing, and lodging together '
            f'before anything is confirmed.\n\n'
            f'With care,\n'
            f'The AfroLink Adventures team\n'
        )
        send_inquiry_mail(
            subject=guest_subject,
            message=guest_body,
            recipient_list=[lead.email],
        )


def _notify_admin_experience_inquiry(inquiry):
    recipients = _inquiry_notify_recipients()
    if not recipients:
        return

    subject = f'[AfroLink] New experience inquiry from {inquiry.email}'
    extra = inquiry.additional_requirements or 'None provided'
    body = (
        f'A guest submitted an experience inquiry from an empty results state.\n\n'
        f'Name: {inquiry.full_name or "Not provided"}\n'
        f'Email: {inquiry.email}\n'
        f'Context: {inquiry.context_label or "Not provided"}\n'
        f'Page: {inquiry.page_url or "Not provided"}\n'
        f'Submitted: {inquiry.created_at:%Y-%m-%d %H:%M %Z}\n\n'
        f'What they are looking for:\n{inquiry.message}\n\n'
        f'Additional requirements:\n{extra}\n'
    )
    send_inquiry_mail(
        subject=subject,
        message=body,
        recipient_list=recipients,
    )


@require_POST
def submit_experience_inquiry(request):
    message = (request.POST.get('message') or '').strip()
    email = (request.POST.get('email') or '').strip()
    full_name = (request.POST.get('full_name') or '').strip()[:255]
    additional_requirements = (
        request.POST.get('additional_requirements') or ''
    ).strip()
    page_url = (request.POST.get('page_url') or request.META.get('HTTP_REFERER') or '')[
        :500
    ]
    context_label = (request.POST.get('context_label') or '')[:255]

    errors = {}
    if not full_name:
        errors['full_name'] = _('Please enter your name.')
    if not message:
        errors['message'] = _('Please tell us what you are looking for.')
    elif len(message) < 10:
        errors['message'] = _('Please share a little more detail (at least 10 characters).')
    elif len(message) > 4000:
        errors['message'] = _('Please keep your request under 4000 characters.')

    if len(additional_requirements) > 4000:
        errors['additional_requirements'] = _(
            'Please keep additional requirements under 4000 characters.'
        )

    if not email:
        errors['email'] = _('Please enter your email address.')
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = _('Please enter a valid email address.')

    if errors:
        return JsonResponse(
            {
                'ok': False,
                'errors': errors,
                'message': _('Please correct the highlighted fields.'),
            },
            status=400,
        )

    inquiry = ExperienceInquiry.objects.create(
        full_name=strip_tags(full_name),
        email=email,
        message=strip_tags(message),
        additional_requirements=strip_tags(additional_requirements),
        page_url=page_url,
        context_label=strip_tags(context_label),
    )
    _notify_admin_experience_inquiry(inquiry)

    track(
        event_type=EngagementEvent.EventType.INQUIRY_SUBMIT,
        object_type=EngagementEvent.ObjectType.EXPERIENCE_INQUIRY,
        object_id=inquiry.id,
        object_label=email,
        metadata={
            'page_url': page_url[:500],
            'context_label': context_label[:255],
        },
        request=request,
    )

    success = _(
        'Thank you — we received your inquiry and will be in touch shortly.'
    )
    return JsonResponse({'ok': True, 'message': success})
