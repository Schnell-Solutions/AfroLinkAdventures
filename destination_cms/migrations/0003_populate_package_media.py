from django.db import migrations


PACKAGE_MEDIA = {
    'executive-equator-wilderness-challenge': {
        'summary_en': (
            'A compact executive route linking Nairobi parkland golf, Rift Valley water safaris, '
            'Mount Kenya highland recovery, and a coastal Baobab Course finish.'
        ),
        'summary_de': (
            'Eine kompakte Executive-Route mit Nairobi-Parkland-Golf, Rift-Valley-Wassersafaris, '
            'Mount-Kenya-Erholung und einem Baobab-Course-Finale an der Kueste.'
        ),
        'card_image_url': (
            'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?'
            'auto=format&fit=crop&w=1200&q=80'
        ),
        'hero_image_url': (
            'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?'
            'auto=format&fit=crop&w=1800&q=80'
        ),
    },
    'ultimate-odyssey': {
        'summary_en': (
            'The complete AfroLink circuit for guests who want a slower, more cinematic progression '
            'through championship golf, private conservancy access, Tsavo wilderness, and the coast.'
        ),
        'summary_de': (
            'Die vollstaendige AfroLink-Runde fuer Gaeste, die eine ruhigere, filmische Abfolge aus '
            'Championship-Golf, privaten Schutzgebieten, Tsavo-Wildnis und Kueste suchen.'
        ),
        'card_image_url': (
            'https://images.unsplash.com/photo-1535941339077-2dd1c7963098?'
            'auto=format&fit=crop&w=1200&q=80'
        ),
        'hero_image_url': (
            'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?'
            'auto=format&fit=crop&w=1800&q=80'
        ),
    },
}


def populate_package_media(apps, schema_editor):
    base_package = apps.get_model('destination_cms', 'BasePackage')

    for slug, payload in PACKAGE_MEDIA.items():
        base_package.objects.filter(slug=slug).update(**payload)


def clear_package_media(apps, schema_editor):
    base_package = apps.get_model('destination_cms', 'BasePackage')
    base_package.objects.filter(slug__in=PACKAGE_MEDIA.keys()).update(
        summary_en='',
        summary_de='',
        card_image_url='',
        hero_image_url='',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0002_basepackage_card_image_url_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_package_media, clear_package_media),
    ]
