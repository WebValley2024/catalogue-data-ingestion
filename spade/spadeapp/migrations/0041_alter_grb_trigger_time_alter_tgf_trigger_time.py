# Generated by Django 4.2.13 on 2024-07-02 13:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0040_alter_earthquake_locationsource_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 2, 13, 39, 12, 702068, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 2, 13, 39, 12, 701071, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
