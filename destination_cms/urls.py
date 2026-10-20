from django.urls import path
from django.views.generic import RedirectView

from .views import (
    AccommodationDetailView,
    CourseDetailView,
    CourseListView,
    GolfEventDetailView,
    GolfEventListView,
    JournalArticleDetailView,
    PackageDetailView,
    PackageListView,
    RegionListView,
    RegionalHubView,
    SafariDetailView,
    SafariListView,
    WellnessDetailView,
)

app_name = 'destination_cms'

urlpatterns = [
    path('regions/', RegionListView.as_view(), name='region_list'),
    path('regions/<slug:slug>/', RegionalHubView.as_view(), name='region_hub'),
    path('journeys/', PackageListView.as_view(), name='package_list'),
    path('journeys/<slug:slug>/', PackageDetailView.as_view(), name='package_detail'),
    path('events/', GolfEventListView.as_view(), name='event_list'),
    path('events/<slug:slug>/', GolfEventDetailView.as_view(), name='event_detail'),
    path('accommodations/<slug:slug>/', AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('journal/<slug:slug>/', JournalArticleDetailView.as_view(), name='journal_detail'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path(
        'golf/',
        RedirectView.as_view(pattern_name='destination_cms:course_list', permanent=True),
        name='course_list_legacy',
    ),
    path('safaris/', SafariListView.as_view(), name='safari_list'),
    path('safaris/<slug:slug>/', SafariDetailView.as_view(), name='safari_detail'),
    path(
        'safari/',
        RedirectView.as_view(pattern_name='destination_cms:safari_list', permanent=True),
        name='safari_list_legacy',
    ),
    path('wellness/<slug:slug>/', WellnessDetailView.as_view(), name='wellness_detail'),
]
