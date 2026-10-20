from django.db import migrations


SAFARI_SLUGS = {
    'Nairobi National Park': 'nairobi-national-park',
    'Lake Naivasha Hippo Safaris': 'lake-naivasha-hippo-safaris',
    'Crescent Island Walking Safaris': 'crescent-island-walking-safaris',
    'Ol Pejeta Conservancy': 'ol-pejeta-conservancy',
    'Tsavo East/West National Parks': 'tsavo-east-west-national-parks',
}


GALLERY_IMAGES = [
    ('golfcourse', 'slug', 'karen-country-club', 'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&w=1200&q=80', 'Tree-lined Nairobi parkland routing and approach angles.', 'Baumgesaeumtes Nairobi-Parkland-Routing und Angriffswinkel.'),
    ('golfcourse', 'slug', 'karen-country-club', 'https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?auto=format&fit=crop&w=1200&q=80', 'Green complex discipline and mature fairway corridors.', 'Gruenkomplex-Disziplin und reife Fairway-Korridore.'),
    ('golfcourse', 'slug', 'muthaiga-golf-club', 'https://images.unsplash.com/photo-1592919505780-303950717480?auto=format&fit=crop&w=1200&q=80', 'Championship tee strategy and tournament-conditioned surfaces.', 'Championship-Tee-Strategie und turnierfaehige Spielflaechen.'),
    ('golfcourse', 'slug', 'muthaiga-golf-club', 'https://images.unsplash.com/photo-1600679472829-3044539ce8ed?auto=format&fit=crop&w=1200&q=80', 'Approach precision into protected Nairobi greens.', 'Praezise Annaherung in geschuetzte Nairobi-Gruens.'),
    ('golfcourse', 'slug', 'windsor-golf-country-club', 'https://images.unsplash.com/photo-1535132011086-b8818f016104?auto=format&fit=crop&w=1200&q=80', 'Forest-estate routing with patient par-five decision points.', 'Forest-Estate-Routing mit geduldigen Par-5-Entscheidungen.'),
    ('golfcourse', 'slug', 'great-rift-valley-lodge-golf-resort', 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80', 'Escarpment golf shaped by elevation, wind, and release.', 'Escarpment-Golf gepraegt von Hoehe, Wind und Ballrelease.'),
    ('golfcourse', 'slug', 'fairmont-mount-kenya-safari-club', 'https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?auto=format&fit=crop&w=1200&q=80', 'Highland air and equator-line short-game calibration.', 'Highland-Luft und Short-Game-Kalibrierung an der Aequatorlinie.'),
    ('golfcourse', 'slug', 'vipingo-ridge-baobab-course', 'https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?auto=format&fit=crop&w=1200&q=80', 'Coastal shot-making and wind-first Baobab Course strategy.', 'Kuesten-Shot-Making und windorientierte Baobab-Course-Strategie.'),
    ('safariextension', 'slug', 'nairobi-national-park', 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80', 'Big game viewing framed by Nairobi access and golf timing.', 'Grosswildbeobachtung mit Nairobi-Zugang und Golf-Timing.'),
    ('safariextension', 'slug', 'lake-naivasha-hippo-safaris', 'https://images.unsplash.com/photo-1547970810-dc1eac37d174?auto=format&fit=crop&w=1200&q=80', 'Lake Naivasha water safaris, hippo channels, and birdlife.', 'Lake-Naivasha-Wassersafaris, Hippo-Kanaele und Vogelwelt.'),
    ('safariextension', 'slug', 'crescent-island-walking-safaris', 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=1200&q=80', 'Walking safari terrain for quiet movement between golf days.', 'Walking-Safari-Gelaende fuer ruhige Bewegung zwischen Golftagen.'),
    ('safariextension', 'slug', 'ol-pejeta-conservancy', 'https://images.unsplash.com/photo-1549366021-9f761d040a94?auto=format&fit=crop&w=1200&q=80', 'Rhino conservation and private conservancy predator tracking.', 'Nashornschutz und Predator-Tracking in privater Conservancy.'),
    ('safariextension', 'slug', 'tsavo-east-west-national-parks', 'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?auto=format&fit=crop&w=1200&q=80', 'Tsavo wilderness, red-earth elephant country, and coastal extensions.', 'Tsavo-Wildnis, rote Elefantenerde und Kuesten-Erweiterungen.'),
]


def get_content_type(content_type_model, model_name):
    content_type, _ = content_type_model.objects.get_or_create(
        app_label='destination_cms',
        model=model_name,
    )
    return content_type


def populate_detail_page_data(apps, schema_editor):
    content_type_model = apps.get_model('contenttypes', 'ContentType')
    gallery_image = apps.get_model('destination_cms', 'GalleryImage')
    golf_course = apps.get_model('destination_cms', 'GolfCourse')
    safari_extension = apps.get_model('destination_cms', 'SafariExtension')

    for name, slug in SAFARI_SLUGS.items():
        safari_extension.objects.filter(name=name).update(slug=slug)

    model_map = {
        'golfcourse': golf_course,
        'safariextension': safari_extension,
    }
    known_image_urls = [payload[3] for payload in GALLERY_IMAGES]
    gallery_image.objects.filter(image_url__in=known_image_urls).delete()

    counters = {}
    records = []
    for model_name, lookup_field, lookup_value, image_url, caption_en, caption_de in GALLERY_IMAGES:
        content_object = model_map[model_name].objects.filter(
            **{lookup_field: lookup_value}
        ).first()
        if content_object is None:
            continue

        counter_key = (model_name, content_object.id)
        counters[counter_key] = counters.get(counter_key, 0) + 1
        records.append(
            gallery_image(
                content_type=get_content_type(content_type_model, model_name),
                object_id=content_object.id,
                image_url=image_url,
                caption_en=caption_en,
                caption_de=caption_de,
                display_order=counters[counter_key],
            )
        )

    gallery_image.objects.bulk_create(records)


def clear_detail_page_data(apps, schema_editor):
    gallery_image = apps.get_model('destination_cms', 'GalleryImage')
    safari_extension = apps.get_model('destination_cms', 'SafariExtension')

    known_image_urls = [payload[3] for payload in GALLERY_IMAGES]
    gallery_image.objects.filter(image_url__in=known_image_urls).delete()

    safari_extension.objects.filter(slug__in=SAFARI_SLUGS.values()).update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0004_safariextension_slug'),
    ]

    operations = [
        migrations.RunPython(populate_detail_page_data, clear_detail_page_data),
    ]
