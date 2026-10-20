from django.db import migrations


ACCOMMODATION_SLUGS = {
    'Hemingways Nairobi': 'hemingways-nairobi',
    'Loldia House': 'loldia-house',
    'Fairmont Mount Kenya Safari Club': 'fairmont-mount-kenya-safari-club-accommodation',
    'Vipingo Ridge Private Villas': 'vipingo-ridge-private-villas',
}


ACCOMMODATION_IMAGES = [
    ('hemingways-nairobi', 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80', 'Polished Nairobi garden-suite arrival base.', 'Elegante Nairobi Garden-Suite-Ankunftsbasis.'),
    ('hemingways-nairobi', 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80', 'Private city recovery before Karen and Muthaiga rounds.', 'Private Stadterholung vor Karen- und Muthaiga-Runden.'),
    ('loldia-house', 'https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80', 'Lake Naivasha lodge pacing with quiet water access.', 'Lake-Naivasha-Lodge-Tempo mit ruhigem Wasserzugang.'),
    ('fairmont-mount-kenya-safari-club-accommodation', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80', 'Highland club base for equator golf and mountain air.', 'Highland-Club-Basis fuer Aequatorgolf und Bergluft.'),
    ('vipingo-ridge-private-villas', 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=80', 'Private coastal villa base beside Baobab Course routing.', 'Private Kuestenvillenbasis neben dem Baobab-Course-Routing.'),
]


def get_accommodation_content_type(content_type_model):
    content_type, _ = content_type_model.objects.get_or_create(
        app_label='destination_cms',
        model='accommodation',
    )
    return content_type


def populate_accommodation_data(apps, schema_editor):
    accommodation = apps.get_model('destination_cms', 'Accommodation')
    content_type_model = apps.get_model('contenttypes', 'ContentType')
    gallery_image = apps.get_model('destination_cms', 'GalleryImage')

    for name, slug in ACCOMMODATION_SLUGS.items():
        accommodation.objects.filter(name=name).update(slug=slug)

    known_image_urls = [payload[1] for payload in ACCOMMODATION_IMAGES]
    gallery_image.objects.filter(image_url__in=known_image_urls).delete()

    content_type = get_accommodation_content_type(content_type_model)
    counters = {}
    records = []
    for slug, image_url, caption_en, caption_de in ACCOMMODATION_IMAGES:
        stay = accommodation.objects.filter(slug=slug).first()
        if stay is None:
            continue

        counters[stay.id] = counters.get(stay.id, 0) + 1
        records.append(
            gallery_image(
                content_type=content_type,
                object_id=stay.id,
                image_url=image_url,
                caption_en=caption_en,
                caption_de=caption_de,
                display_order=counters[stay.id],
            )
        )

    gallery_image.objects.bulk_create(records)


def clear_accommodation_data(apps, schema_editor):
    accommodation = apps.get_model('destination_cms', 'Accommodation')
    gallery_image = apps.get_model('destination_cms', 'GalleryImage')

    known_image_urls = [payload[1] for payload in ACCOMMODATION_IMAGES]
    gallery_image.objects.filter(image_url__in=known_image_urls).delete()
    accommodation.objects.filter(slug__in=ACCOMMODATION_SLUGS.values()).update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0006_accommodation_slug'),
    ]

    operations = [
        migrations.RunPython(populate_accommodation_data, clear_accommodation_data),
    ]
