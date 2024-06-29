from django.db import models

# Create your models here.
class SampleModel(models.Model):
    fieldSample = models.CharField(max_length=10)

    def __str__(self):
        return self.fieldSample

class TGF(models.Model):
    TGF_name = models.CharField(max_length=30)
    GEO_long = models.FloatField("geo_long")
    GEO_lat = models.FloatField("geo_lat")
    trigger_time = models.DateTimeField("trigger_time")
    orbit = models.IntegerField("orbit")
    T50 = models.TimeField("T50")
    T50_err = models.TimeField("T50_err")
    T50_err_applied = models.TimeField("T50_err_applied")
    sat_altitude = models.FloatField("sat_altitude")
    ML_counts = models.FloatField("ML_counts")
    ML_counts_err = models.FloatField("ML_counts_err")
    ML_counts_err_applied = models.FloatField("ML_counts_err_applied")
    event_type = models.IntegerField("event_type")
    RA = models.FloatField("RA")
    DEC = models.FloatField("DEC")
    start_time_obs = models.DateTimeField("start_time_obs")
    end_time_obs = models.DateTimeField("end_time_obs")
    reliability = models.FloatField("reliability")

    