# Generated by Django 4.2.13 on 2024-07-02 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spadeapp', '0038_alter_grb_trigger_time_alter_swe_trigger_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='swe',
            name='top',
            field=models.CharField(default='', max_length=10, verbose_name='top'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='depth',
            field=models.FloatField(blank=True, verbose_name='depth'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='depth_err',
            field=models.CharField(blank=True, max_length=50, verbose_name='depth_err'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='dmin',
            field=models.CharField(blank=True, max_length=50, verbose_name='Dmin'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='gap',
            field=models.CharField(blank=True, max_length=50, verbose_name='Gap'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='horizontal_err',
            field=models.CharField(blank=True, max_length=50, verbose_name='horizontal_err'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='identifier',
            field=models.CharField(blank=True, max_length=20, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='latitude',
            field=models.FloatField(blank=True, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='locationSource',
            field=models.CharField(blank=True, default='us', max_length=5, verbose_name='Location source'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='longitude',
            field=models.FloatField(blank=True, verbose_name='longitude'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='magSource',
            field=models.CharField(blank=True, default='us', max_length=20, verbose_name='Magnitude source'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='magType',
            field=models.CharField(blank=True, max_length=50, verbose_name='Magnitude type'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='magnitude',
            field=models.FloatField(blank=True, max_length=50, verbose_name='magnitude'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='magnitude_err',
            field=models.CharField(blank=True, max_length=50, verbose_name='magnitude_err'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='magnst',
            field=models.CharField(blank=True, max_length=50, verbose_name='Magnst'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='net',
            field=models.CharField(blank=True, max_length=2, verbose_name='Net'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='nst',
            field=models.CharField(blank=True, max_length=50, verbose_name='Nst'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='place',
            field=models.CharField(blank=True, max_length=50, verbose_name='Place'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='rms',
            field=models.CharField(blank=True, max_length=50, verbose_name='Rms'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='sat_source',
            field=models.CharField(blank=True, max_length=50, verbose_name='Satellite'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='status',
            field=models.CharField(blank=True, default='0', max_length=50, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='trigger_time',
            field=models.DateTimeField(blank=True, verbose_name='trigger_time'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='type',
            field=models.CharField(blank=True, max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='updated',
            field=models.CharField(blank=True, default='loaded', max_length=20, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='BAT_DEC',
            field=models.CharField(blank=True, max_length=50, verbose_name='BAT_DEC'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='BAT_RA',
            field=models.CharField(blank=True, max_length=50, verbose_name='BAT_RA'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='BAT_T90',
            field=models.CharField(blank=True, default='-', max_length=50, verbose_name='BAT_T90'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='BAT_fluence',
            field=models.CharField(blank=True, max_length=50, verbose_name='Bat fluence'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='DEC',
            field=models.CharField(blank=True, default='0', max_length=50, verbose_name='DEC'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='RA',
            field=models.CharField(blank=True, default='0', max_length=50, verbose_name='RA'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='T90',
            field=models.CharField(blank=True, max_length=50, verbose_name='T90 (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='end_time_obs',
            field=models.CharField(blank=True, max_length=50, verbose_name='End time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='geo_lat',
            field=models.CharField(blank=True, max_length=50, verbose_name='Geo latitude (deg)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='geo_long',
            field=models.CharField(blank=True, max_length=50, verbose_name='Geo longitude (deg)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='max_count',
            field=models.CharField(blank=True, max_length=50, verbose_name='Max count'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='normalised_duration',
            field=models.CharField(blank=True, default='-', max_length=50, verbose_name='normalised_duration'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='reliability',
            field=models.CharField(blank=True, max_length=50, verbose_name='Reliability'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='sat_source',
            field=models.CharField(blank=True, max_length=50, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='sigma',
            field=models.CharField(blank=True, max_length=50, verbose_name='Sigma'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='start_time_obs',
            field=models.CharField(blank=True, max_length=50, verbose_name='Start time observations (s)'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='trigger_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 2, 10, 29, 17, 255330, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='type',
            field=models.CharField(blank=True, max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='grb',
            name='xrt_spectral_index',
            field=models.CharField(blank=True, max_length=50, verbose_name='xrt spectral index'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='flux',
            field=models.CharField(blank=True, max_length=5, verbose_name='Flux'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='region',
            field=models.CharField(blank=True, max_length=20, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='sat_source',
            field=models.CharField(blank=True, max_length=50, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='time_end_obs',
            field=models.CharField(blank=True, max_length=50, verbose_name='Time end observations'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='time_start_obs',
            field=models.CharField(blank=True, max_length=50, verbose_name='Time start observations'),
        ),
        migrations.AlterField(
            model_name='swe',
            name='trigger_time',
            field=models.DateTimeField(blank=True, verbose_name='Trigger time'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='DEC',
            field=models.CharField(blank=True, max_length=50, verbose_name='DEC'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='GEO_lat',
            field=models.CharField(blank=True, max_length=50, verbose_name='Geo latitude'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='GEO_long',
            field=models.CharField(blank=True, max_length=50, verbose_name='Geo longitude'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='ML_counts',
            field=models.CharField(blank=True, max_length=50, verbose_name='ML counts'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='ML_counts_err',
            field=models.CharField(blank=True, max_length=50, verbose_name='ML counts error'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='ML_counts_err_applied',
            field=models.CharField(blank=True, max_length=50, verbose_name='ML counts error applied'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='RA',
            field=models.CharField(blank=True, max_length=50, verbose_name='RA'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='T50',
            field=models.CharField(blank=True, max_length=50, verbose_name='T50'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='T50_err',
            field=models.CharField(blank=True, max_length=50, verbose_name='T50 error'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='T50_err_applied',
            field=models.CharField(blank=True, max_length=50, verbose_name='T50 error applied'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='TGF_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='TGF name'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='end_time_obs',
            field=models.CharField(blank=True, max_length=50, verbose_name='End time observations'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='event_type',
            field=models.CharField(blank=True, max_length=50, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='normalised_duration',
            field=models.CharField(blank=True, default='1', max_length=50, verbose_name='Normalised duration'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='orbit',
            field=models.CharField(blank=True, max_length=50, verbose_name='Orbit'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='reliability',
            field=models.CharField(blank=True, max_length=50, verbose_name='Reliability'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='sat_altitude',
            field=models.CharField(blank=True, max_length=50, verbose_name='Satellite altitude'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='sat_source',
            field=models.CharField(blank=True, default='Fermi', max_length=50, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='start_time_obs',
            field=models.CharField(blank=True, max_length=50, verbose_name='Start time observations'),
        ),
        migrations.AlterField(
            model_name='tgf',
            name='trigger_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 2, 10, 29, 17, 255330, tzinfo=datetime.timezone.utc), verbose_name='Trigger time'),
        ),
    ]
