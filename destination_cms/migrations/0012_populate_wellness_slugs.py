from django.db import migrations
from django.utils.text import slugify


def populate_wellness_slugs(apps, schema_editor):
    wellness_experience = apps.get_model(
        'destination_cms',
        'WellnessExperience',
    )

    for wellness in wellness_experience.objects.filter(slug__isnull=True):
        base_slug = slugify(wellness.name_en) or f'wellness-{wellness.pk}'
        slug = base_slug
        counter = 2

        while wellness_experience.objects.filter(slug=slug).exclude(
            pk=wellness.pk
        ).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        wellness.slug = slug
        wellness.save(update_fields=['slug'])


def clear_wellness_slugs(apps, schema_editor):
    wellness_experience = apps.get_model(
        'destination_cms',
        'WellnessExperience',
    )
    wellness_experience.objects.update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0011_wellnessexperience_slug'),
    ]

    operations = [
        migrations.RunPython(populate_wellness_slugs, clear_wellness_slugs),
    ]
