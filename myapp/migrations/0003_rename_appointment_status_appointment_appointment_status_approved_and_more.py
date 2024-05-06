# Generated by Django 5.0.4 on 2024-05-01 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_appointment_appointment_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='appointment_status',
            new_name='appointment_status_approved',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_status_cancle',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_status_pandding',
            field=models.BooleanField(default=False),
        ),
    ]
