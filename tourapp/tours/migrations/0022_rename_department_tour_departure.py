# Generated by Django 5.0.4 on 2024-05-07 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0021_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tour',
            old_name='department',
            new_name='departure',
        ),
    ]
