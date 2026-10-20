import django.db.models.deletion
from django.db import migrations, models


def rename_safari_content_type(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ContentType.objects.filter(
        app_label='destination_cms',
        model='safariextension',
    ).update(model='safaridestination')


def revert_safari_content_type(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ContentType.objects.filter(
        app_label='destination_cms',
        model='safaridestination',
    ).update(model='safariextension')


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('destination_cms', '0023_experience_fields_and_relations'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameModel(
                    old_name='SafariExtension',
                    new_name='SafariDestination',
                ),
                migrations.AlterModelOptions(
                    name='safaridestination',
                    options={
                        'ordering': ['region__name_en', 'name'],
                        'verbose_name': 'Safari Destination',
                        'verbose_name_plural': 'Safari Destinations',
                    },
                ),
                migrations.AlterModelTable(
                    name='safaridestination',
                    table='destination_cms_safariextension',
                ),
                migrations.AlterField(
                    model_name='safaridestination',
                    name='region',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='safari_destinations',
                        to='destination_cms.region',
                    ),
                ),
                migrations.AlterField(
                    model_name='dayactivity',
                    name='content_type',
                    field=models.ForeignKey(
                        limit_choices_to={
                            'app_label': 'destination_cms',
                            'model__in': [
                                'golfcourse',
                                'safaridestination',
                                'safariextension',
                                'wellnessexperience',
                            ],
                        },
                        on_delete=django.db.models.deletion.CASCADE,
                        to='contenttypes.contenttype',
                    ),
                ),
            ],
            database_operations=[
                migrations.RunPython(
                    rename_safari_content_type,
                    revert_safari_content_type,
                ),
            ],
        ),
    ]
