# Generated by Django 4.2.13 on 2024-07-01 15:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0013_earthquake_updated_alter_earthquake_trigger_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earthquake',
            name='trigger_time',
            field=models.CharField(max_length=50, verbose_name='trigger_time'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='end_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 15, 37, 0, 671973, tzinfo=datetime.timezone.utc), verbose_name='End time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='start_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 15, 37, 0, 671973, tzinfo=datetime.timezone.utc), verbose_name='Start time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 15, 37, 0, 671973, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='end_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 15, 37, 0, 669978, tzinfo=datetime.timezone.utc), verbose_name='End time observations'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='start_time_obs',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 15, 37, 0, 669978, tzinfo=datetime.timezone.utc), verbose_name='Start time observations'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 15, 37, 0, 669978, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
