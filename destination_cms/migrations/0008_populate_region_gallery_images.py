from django.db import migrations


REGION_IMAGES = [
    ('nairobi-environs', 'https://images.unsplash.com/photo-1489392191049-fc10c97e64b6?auto=format&fit=crop&w=1400&q=80', 'Nairobi access, private city pacing, and parkland golf corridors.', 'Nairobi-Zugang, privates Stadttempo und Parkland-Golfkorridore.'),
    ('nairobi-environs', 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1400&q=80', 'Wildlife viewing within reach of Karen, Muthaiga, and Windsor.', 'Wildbeobachtung in Reichweite von Karen, Muthaiga und Windsor.'),
    ('great-rift-valley', 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1400&q=80', 'Escarpment light, lake safaris, and elevated golf routing.', 'Escarpment-Licht, Seesafaris und erhoehtes Golf-Routing.'),
    ('mount-kenya-region', 'https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?auto=format&fit=crop&w=1400&q=80', 'Highland air, equator golf, and conservancy access.', 'Highland-Luft, Aequatorgolf und Conservancy-Zugang.'),
    ('coastal-strip', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=80', 'Indian Ocean recovery, Baobab Course routing, and reef walks.', 'Indischer-Ozean-Erholung, Baobab-Course-Routing und Riffspaziergaenge.'),
]


def get_region_content_type(content_type_model):
    content_type, _ = content_type_model.objects.get_or_create(
        app_label='destination_cms',
        model='region',
    )
    return content_type


def populate_region_images(apps, schema_editor):
    content_type_model = apps.get_model('contenttypes', 'ContentType')
    gallery_image = apps.get_model('destination_cms', 'GalleryImage')
    region = apps.get_model('destination_cms', 'Region')

    known_image_urls = [payload[1] for payload in REGION_IMAGES]
    gallery_image.objects.filter(image_url__in=known_image_urls).delete()

    content_type = get_region_content_type(content_type_model)
    counters = {}
    records = []

    for slug, image_url, caption_en, caption_de in REGION_IMAGES:
        regional_hub = region.objects.filter(slug=slug).first()
        if regional_hub is None:
            continue

        counters[regional_hub.id] = counters.get(regional_hub.id, 0) + 1
        records.append(
            gallery_image(
                content_type=content_type,
                object_id=regional_hub.id,
                image_url=image_url,
                caption_en=caption_en,
                caption_de=caption_de,
                display_order=counters[regional_hub.id],
            )
        )

    gallery_image.objects.bulk_create(records)


def clear_region_images(apps, schema_editor):
    gallery_image = apps.get_model('destination_cms', 'GalleryImage')
    known_image_urls = [payload[1] for payload in REGION_IMAGES]
    gallery_image.objects.filter(image_url__in=known_image_urls).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0007_populate_accommodation_slugs_and_gallery_images'),
    ]

    operations = [
        migrations.RunPython(populate_region_images, clear_region_images),
    ]
