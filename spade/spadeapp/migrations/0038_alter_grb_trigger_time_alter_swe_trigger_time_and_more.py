# Generated by Django 4.2.13 on 2024-07-02 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0037_alter_earthquake_trigger_time_alter_grb_trigger_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 2, 8, 0, 24, 24744, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='trigger_time',
            field=models.DateTimeField(verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 2, 8, 0, 24, 22750, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
