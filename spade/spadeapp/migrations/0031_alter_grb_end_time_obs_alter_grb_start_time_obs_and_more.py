# Generated by Django 4.2.13 on 2024-07-01 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0030_alter_grb_end_time_obs_alter_grb_references_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grb',
            name='end_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 17, 15, 304749, tzinfo=datetime.timezone.utc), verbose_name='End time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='start_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 17, 15, 304749, tzinfo=datetime.timezone.utc), verbose_name='Start time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 17, 15, 304749, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 17, 15, 300759, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
