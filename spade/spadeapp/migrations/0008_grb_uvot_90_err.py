# Generated by Django 4.2.13 on 2024-06-29 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0007_grb_xrt_column_density'),
    ]

    operations = [
        migrations.AddField(
            model_name='grb',
            name='uvot_90_err',
            field=models.FloatField(default=0, verbose_name='UVOT 90%/ error'),
            preserve_default=False,
        ),
    ]
