# Generated by Django 5.0.4 on 2024-04-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0007_alter_place_description_alter_tour_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
