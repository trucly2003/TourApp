# Generated by Django 5.0.4 on 2024-05-03 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0015_ticket_date_arrive_ticket_date_depart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='time_arrive',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='time_depart',
        ),
    ]
