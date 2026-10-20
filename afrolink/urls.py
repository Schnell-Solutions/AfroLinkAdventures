"""
URL configuration for afrolink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.i18n import set_language

import afrolink.admin  # noqa: F401 — site branding
from destination_cms.views import HomeView, JournalArticleListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('i18n/setlang/', set_language, name='set_language'),
    path(
        'privacy/',
        TemplateView.as_view(template_name='privacy.html'),
        name='privacy',
    ),
    path(
        'about/',
        TemplateView.as_view(template_name='destination_cms/about.html'),
        name='about',
    ),
    path(
        'journal/',
        JournalArticleListView.as_view(),
        name='journal',
    ),
    path(
        'terms/',
        TemplateView.as_view(template_name='terms.html'),
        name='terms',
    ),
    path(
        'legal/',
        TemplateView.as_view(template_name='legal_notice.html'),
        name='legal',
    ),
    path('', include('destination_cms.urls')),
    path('', include('inquiry_crm.urls')),
    path('analytics/', include('analytics.urls')),
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
]
