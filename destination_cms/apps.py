from django.apps import AppConfig


class DestinationCmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'destination_cms'
    verbose_name = 'Destinations & journeys'

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = 'AfroLink Adventures'
        admin.site.site_title = 'AfroLink Adventures Admin'
        admin.site.index_title = 'Journeys, destinations, inquiries & promotions'
