# Generated by Django 5.0.4 on 2024-05-05 14:55

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0017_alter_tour_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='booking_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tour',
            name='arrival',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tour',
            name='department',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('payment_method', models.CharField(max_length=255)),
                ('payment_dated', models.DateTimeField(auto_now=True)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tours.ticket')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
