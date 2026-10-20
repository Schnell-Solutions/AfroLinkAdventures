from django.db import migrations


PARTNERS = [
    {
        'name': 'Karen Country Club',
        'logo_path': 'images/partners/karen-country-club-logo.jpg',
        'display_order': 10,
    },
    {
        'name': 'Muthaiga Golf Club',
        'logo_path': 'images/partners/muthaiga-golf-club-logo.png',
        'display_order': 20,
    },
    {
        'name': 'Royal Nairobi Golf Club',
        'logo_path': 'images/partners/royal-nairobi-golf-club-logo.png',
        'display_order': 30,
    },
    {
        'name': 'Sigona Golf Club',
        'logo_path': 'images/partners/sigona-golf-club-logo.png',
        'display_order': 40,
    },
    {
        'name': 'Vipingo Ridge',
        'logo_path': 'images/partners/vipingo-ridge-gold-logo.png',
        'display_order': 50,
    },
    {
        'name': 'Windsor Golf & Country Club',
        'logo_path': 'images/partners/windsor-golf-country-club-logo.jpg',
        'display_order': 60,
    },
]


def populate_partners(apps, schema_editor):
    partner = apps.get_model('destination_cms', 'Partner')
    partner.objects.filter(name__in=[item['name'] for item in PARTNERS]).delete()
    partner.objects.bulk_create(partner(**item) for item in PARTNERS)


def clear_partners(apps, schema_editor):
    partner = apps.get_model('destination_cms', 'Partner')
    partner.objects.filter(name__in=[item['name'] for item in PARTNERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0013_partner'),
    ]

    operations = [
        migrations.RunPython(populate_partners, clear_partners),
    ]
