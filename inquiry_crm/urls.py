from django.urls import path
from django.views.generic import RedirectView

from .views import (
    CustomPlannerView,
    InquiryConfirmationView,
    InquiryIntakeView,
    InquiryStartView,
    add_interest_to_inquiry_list,
    add_to_inquiry_list,
    package_enquiry,
    remove_from_inquiry_list,
    submit_experience_inquiry,
)

app_name = 'inquiry_crm'

urlpatterns = [
    # Legacy CRM package routes → live journeys catalogue
    path(
        'itineraries/',
        RedirectView.as_view(
            pattern_name='destination_cms:package_list',
            permanent=False,
        ),
        name='package_list',
    ),
    path(
        'itineraries/<slug:slug>/',
        RedirectView.as_view(
            pattern_name='destination_cms:package_detail',
            permanent=False,
        ),
        name='itinerary_detail',
    ),
    path(
        'inquiry/package/<slug:slug>/',
        package_enquiry,
        name='package_enquiry',
    ),
    path(
        'journeys/<slug:slug>/add-to-inquiry-list/',
        add_to_inquiry_list,
        name='add_to_inquiry_list',
    ),
    path(
        'inquiry/add-interest/',
        add_interest_to_inquiry_list,
        name='add_interest_to_inquiry_list',
    ),
    path(
        'inquiry/remove-item/',
        remove_from_inquiry_list,
        name='remove_from_inquiry_list',
    ),
    path(
        'inquiry/experience/',
        submit_experience_inquiry,
        name='submit_experience_inquiry',
    ),
    path('planner/', CustomPlannerView.as_view(), name='custom_planner'),
    path('custom-itinerary/', CustomPlannerView.as_view(), name='custom_itinerary'),
    path('consultation/', InquiryStartView.as_view(), name='consultation'),
    path('start/', InquiryStartView.as_view(), name='inquiry_start'),
    path('custom-package/', InquiryIntakeView.as_view(), name='custom_package'),
    path('inquiry/', InquiryStartView.as_view(), name='start_inquiry'),
    path('inquiry/intake/', InquiryIntakeView.as_view(), name='inquiry_intake'),
    path(
        'inquiry/confirmation/<str:token>/',
        InquiryConfirmationView.as_view(),
        name='inquiry_confirmation',
    ),
]
