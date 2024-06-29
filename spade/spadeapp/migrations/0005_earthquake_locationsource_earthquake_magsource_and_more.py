# Generated by Django 4.2.13 on 2024-06-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0004_earthquake_grb_swe_tgf_sat_source_alter_tgf_geo_lat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='earthquake',
            name='locationSource',
            field=models.CharField(default='us', max_length=5, verbose_name='Location source'),
        ),
        migrations.AddField(
            model_name='earthquake',
            name='magSource',
            field=models.CharField(default='us', max_length=20, verbose_name='Magnitude source'),
        ),
        migrations.AddField(
            model_name='earthquake',
            name='source',
            field=models.CharField(default='earthquake', max_length=20, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='sat_source',
            field=models.CharField(max_length=50, verbose_name='Satellite'),
        ),
    ]
