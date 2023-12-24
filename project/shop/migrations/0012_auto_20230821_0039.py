# Generated by Django 2.2 on 2023-08-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20230821_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img1',
            field=models.URLField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='img2',
            field=models.URLField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='img3',
            field=models.URLField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='logo_url',
            field=models.URLField(blank=True, default=True),
        ),
    ]
