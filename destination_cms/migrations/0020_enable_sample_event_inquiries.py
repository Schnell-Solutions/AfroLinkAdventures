from django.db import migrations


def enable_sample_event_inquiries(apps, schema_editor):
    golf_event = apps.get_model('destination_cms', 'GolfEvent')
    golf_event.objects.filter(
        slug='vipingo-ridge-coastal-invitational',
    ).update(accepts_inquiries=True)


def disable_sample_event_inquiries(apps, schema_editor):
    golf_event = apps.get_model('destination_cms', 'GolfEvent')
    golf_event.objects.filter(
        slug='vipingo-ridge-coastal-invitational',
    ).update(accepts_inquiries=False)


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0019_golfevent_accepts_inquiries'),
    ]

    operations = [
        migrations.RunPython(
            enable_sample_event_inquiries,
            disable_sample_event_inquiries,
        ),
    ]
