from django.db import migrations


def promote_sample_event(apps, schema_editor):
    golf_event = apps.get_model('destination_cms', 'GolfEvent')
    golf_event.objects.filter(
        slug='vipingo-ridge-coastal-invitational',
    ).update(
        is_promoted=True,
        promotion_priority=10,
    )


def clear_sample_promotion(apps, schema_editor):
    golf_event = apps.get_model('destination_cms', 'GolfEvent')
    golf_event.objects.filter(
        slug='vipingo-ridge-coastal-invitational',
    ).update(
        is_promoted=False,
        promotion_priority=100,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0017_alter_golfevent_options_golfevent_is_promoted_and_more'),
    ]

    operations = [
        migrations.RunPython(promote_sample_event, clear_sample_promotion),
    ]
