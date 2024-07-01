# Generated by Django 4.2.13 on 2024-07-01 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0020_alter_grb_end_time_obs_alter_grb_start_time_obs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grb',
            name='end_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 22, 22, 288240, tzinfo=datetime.timezone.utc), verbose_name='End time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='start_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 22, 22, 288240, tzinfo=datetime.timezone.utc), verbose_name='Start time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 22, 22, 288240, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='end_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 22, 22, 287243, tzinfo=datetime.timezone.utc), verbose_name='End time observations'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='event_type',
            field=models.FloatField(verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='start_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 22, 22, 287243, tzinfo=datetime.timezone.utc), verbose_name='Start time observations'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 22, 22, 287243, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
