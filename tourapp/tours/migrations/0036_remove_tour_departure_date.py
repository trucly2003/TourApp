# Generated by Django 5.0.4 on 2024-05-20 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0035_remove_booking_adults_remove_booking_create_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='departure_date',
        ),
    ]
