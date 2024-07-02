# Generated by Django 4.2.13 on 2024-07-01 19:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0033_alter_grb_reliability_alter_grb_trigger_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grb',
            name='geo_lat',
            field=models.CharField(max_length=50, verbose_name='Geo latitude (deg)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='geo_long',
            field=models.CharField(max_length=50, verbose_name='Geo longitude (deg)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 36, 39, 367906, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 36, 39, 366909, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
