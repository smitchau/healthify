# Generated by Django 5.0.4 on 2024-05-01 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_appointment_status_appointment_appointment_status_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_status_pandding',
            field=models.BooleanField(default=True),
        ),
    ]