from datetime import date, time

from django.db import migrations


EVENTS = [
    {
        'title_en': 'Tuesday Nairobi Members Guest Round',
        'title_de': 'Dienstag Nairobi Members Guest Round',
        'slug': 'tuesday-nairobi-members-guest-round',
        'region_slug': 'nairobi-environs',
        'course_slug': 'muthaiga-golf-club',
        'summary_en': (
            'A recurring Tuesday golf day suitable for visitors who want a structured club experience '
            'while staying close to Nairobi routing.'
        ),
        'summary_de': (
            'Ein wiederkehrender Dienstag-Golftag fuer Gaeste, die ein strukturiertes Club-Erlebnis '
            'nahe der Nairobi-Route wuenschen.'
        ),
        'event_date': date(2026, 8, 4),
        'start_time': time(9, 0),
        'recurrence': 'weekly',
        'recurrence_weekday': 1,
        'image_url': 'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&w=1400&q=80',
    },
    {
        'title_en': 'Vipingo Ridge Coastal Invitational',
        'title_de': 'Vipingo Ridge Coastal Invitational',
        'slug': 'vipingo-ridge-coastal-invitational',
        'region_slug': 'coastal-strip',
        'course_slug': 'vipingo-ridge-baobab-course',
        'summary_en': (
            'A coastal tournament-style golf event pairing Indian Ocean play with private post-round '
            'recovery and lodge routing.'
        ),
        'summary_de': (
            'Ein kuestenorientiertes Turnierformat mit Indian-Ocean-Golf, privater Erholung nach der '
            'Runde und Lodge-Routing.'
        ),
        'event_date': date(2026, 9, 18),
        'start_time': time(8, 30),
        'recurrence': 'none',
        'recurrence_weekday': None,
        'image_url': 'https://images.unsplash.com/photo-1592919505780-303950717480?auto=format&fit=crop&w=1400&q=80',
    },
]


def populate_events(apps, schema_editor):
    golf_event = apps.get_model('destination_cms', 'GolfEvent')
    region = apps.get_model('destination_cms', 'Region')
    golf_course = apps.get_model('destination_cms', 'GolfCourse')

    golf_event.objects.filter(slug__in=[event['slug'] for event in EVENTS]).delete()

    records = []
    for event in EVENTS:
        event = event.copy()
        region_slug = event.pop('region_slug')
        course_slug = event.pop('course_slug')
        event_region = region.objects.filter(slug=region_slug).first()
        if event_region is None:
            continue
        event['region'] = event_region
        event['golf_course'] = golf_course.objects.filter(slug=course_slug).first()
        records.append(golf_event(**event))

    golf_event.objects.bulk_create(records)


def clear_events(apps, schema_editor):
    golf_event = apps.get_model('destination_cms', 'GolfEvent')
    golf_event.objects.filter(slug__in=[event['slug'] for event in EVENTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0015_golfevent'),
    ]

    operations = [
        migrations.RunPython(populate_events, clear_events),
    ]
