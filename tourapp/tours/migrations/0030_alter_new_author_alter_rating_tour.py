# Generated by Django 5.0.4 on 2024-05-19 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0029_new_author_new_date_post_new_image_alter_new_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.staff'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='tours.tour'),
        ),
    ]