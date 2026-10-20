from datetime import timedelta
from zoneinfo import ZoneInfo

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from destination_cms.models import BasePackage, GolfEvent, Region
from inquiry_crm.models import ExperienceInquiry, Inquiry, InquiryInterest, Lead
from inquiry_crm.tokens import (
    earliest_allowed_consultation_date,
    sign_inquiry_confirmation,
    unsign_inquiry_confirmation,
)


class InquiryTokenTests(TestCase):
    def test_sign_and_unsign_roundtrip(self):
        token = sign_inquiry_confirmation(42)
        self.assertEqual(unsign_inquiry_confirmation(token), 42)


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    INQUIRY_NOTIFY_EMAILS=['ops@example.com'],
    DEFAULT_FROM_EMAIL='AfroLink <noreply@example.com>',
)
class InquiryIntakeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.region = Region.objects.create(
            name_en='Test Region',
            name_de='Test Region',
            slug='test-region',
            is_active=True,
        )
        self.package = BasePackage.objects.create(
            title_en='Signature Route',
            title_de='Signature Route',
            slug='signature-route',
            duration_days=7,
            is_active=True,
            package_type=BasePackage.PackageType.SAFARI,
        )

    def _consultation_payload(self, **overrides):
        consult_date = earliest_allowed_consultation_date()
        data = {
            'full_name': 'Ada Lovelace',
            'email': 'ada@example.com',
            'phone': '+254700000000',
            'preferred_language': 'en',
            'preferred_contact': 'email',
            'budget_band': '15_30k',
            'trip_flexibility': 'few_days',
            'guest_count': '2',
            'accommodation_tier': 'standard_luxury',
            'preferred_consultation_date': consult_date.isoformat(),
            'preferred_consultation_window': 'afternoon',
            'luggage_limit_acknowledged': 'on',
            'additional_requirements': 'Prefer private transfers.',
            'intent': 'consultation',
            'day_count': '7',
        }
        data.update(overrides)
        return data

    def test_intake_requires_valid_email(self):
        response = self.client.post(
            reverse('inquiry_crm:inquiry_intake') + '?intent=consultation',
            self._consultation_payload(email='not-an-email'),
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'valid email', status_code=400)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_intake_restores_luggage_checkbox_on_error(self):
        response = self.client.post(
            reverse('inquiry_crm:inquiry_intake') + '?intent=consultation',
            self._consultation_payload(email='bad'),
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            'name="luggage_limit_acknowledged"',
            status_code=400,
        )
        self.assertContains(response, 'checked', status_code=400)

    def test_successful_light_consultation_creates_records_and_emails(self):
        response = self.client.post(
            reverse('inquiry_crm:inquiry_intake') + '?intent=consultation',
            self._consultation_payload(),
        )
        self.assertEqual(response.status_code, 302)
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.lead.full_name, 'Ada Lovelace')
        self.assertEqual(inquiry.lead.phone, '+254700000000')
        self.assertEqual(inquiry.lead.budget_band, '15_30k')
        self.assertTrue(inquiry.luggage_limit_acknowledged)
        self.assertEqual(len(mail.outbox), 2)
        token = sign_inquiry_confirmation(inquiry.id)
        self.assertIn(token, response['Location'])

    def test_confirmation_requires_valid_token(self):
        response = self.client.post(
            reverse('inquiry_crm:inquiry_intake') + '?intent=consultation',
            self._consultation_payload(),
        )
        inquiry = Inquiry.objects.get()
        ok = self.client.get(
            reverse(
                'inquiry_crm:inquiry_confirmation',
                kwargs={'token': sign_inquiry_confirmation(inquiry.id)},
            )
        )
        self.assertEqual(ok.status_code, 200)
        bad = self.client.get(
            reverse(
                'inquiry_crm:inquiry_confirmation',
                kwargs={'token': 'not-a-real-token'},
            )
        )
        self.assertEqual(bad.status_code, 404)

    def test_package_enquiry_increments_session_cart(self):
        # Avoid package_type enum issues by using existing package if create failed shape
        if not self.package.pk:
            self.skipTest('package fixture unavailable')
        response = self.client.get(
            reverse('inquiry_crm:package_enquiry', kwargs={'slug': self.package.slug})
        )
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart = session.get('inquiry_cart', [])
        self.assertTrue(
            any(
                item.get('item_type') == 'package'
                and str(item.get('package_id')) == str(self.package.id)
                for item in cart
            )
        )


class AcceptsInquiriesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.region = Region.objects.create(
            name_en='Event Region',
            name_de='Event Region',
            slug='event-region',
            is_active=True,
        )
        self.closed_event = GolfEvent.objects.create(
            title_en='Closed Event',
            title_de='Closed Event',
            slug='closed-event',
            region=self.region,
            is_active=True,
            accepts_inquiries=False,
            event_date=timezone.now().date() + timedelta(days=30),
            end_date=timezone.now().date() + timedelta(days=32),
        )

    def test_closed_event_cannot_be_shortlisted(self):
        response = self.client.post(
            reverse('inquiry_crm:add_interest_to_inquiry_list'),
            {
                'interest_type': InquiryInterest.InterestType.GOLF_EVENT,
                'object_id': self.closed_event.id,
                'next': '/',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('inquiry_cart', []), [])


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    INQUIRY_NOTIFY_EMAILS=['ops@example.com'],
    DEFAULT_FROM_EMAIL='noreply@example.com',
)
class ExperienceInquiryTests(TestCase):
    def test_requires_name_and_email(self):
        response = self.client.post(
            reverse('inquiry_crm:submit_experience_inquiry'),
            {
                'message': 'Looking for a Masai Mara safari with golf nearby.',
                'email': 'guest@example.com',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['ok'])

    def test_creates_experience_inquiry(self):
        response = self.client.post(
            reverse('inquiry_crm:submit_experience_inquiry'),
            {
                'full_name': 'Guest User',
                'message': 'Looking for a Masai Mara safari with golf nearby.',
                'email': 'guest@example.com',
                'context_label': 'Masai Mara',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['ok'])
        inquiry = ExperienceInquiry.objects.get()
        self.assertEqual(inquiry.full_name, 'Guest User')
        self.assertEqual(inquiry.context_label, 'Masai Mara')
        self.assertEqual(len(mail.outbox), 1)
