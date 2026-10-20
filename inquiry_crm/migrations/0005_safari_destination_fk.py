import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0024_rename_safari_destination'),
        ('inquiry_crm', '0004_inquiry_accommodation_tier_inquiry_target_start_date'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='inquirycustomday',
                    name='safari_extension',
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='inquiry_custom_days',
                        to='destination_cms.safaridestination',
                    ),
                ),
                migrations.AlterField(
                    model_name='inquiryinterest',
                    name='interest_type',
                    field=models.CharField(
                        choices=[
                            ('golf_course', 'Golf Course'),
                            ('safari_extension', 'Safari Destination'),
                            ('accommodation', 'Accommodation'),
                            ('wellness_experience', 'Wellness Experience'),
                            ('golf_event', 'Golf Event'),
                        ],
                        db_index=True,
                        max_length=50,
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
