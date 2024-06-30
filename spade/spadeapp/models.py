from django.db import models
from django.utils import timezone

# Create your models here.
class SampleModel(models.Model):
    fieldSample = models.CharField(max_length=10)
    num = models.IntegerField()

    def __str__(self):
        return self.fieldSample
    
class Earthquake(models.Model):
    sat_source = models.CharField(verbose_name="Satellite", max_length=50)
    trigger_time = models.CharField(verbose_name="trigger_time", max_length=50)
    latitude = models.FloatField("latitude")
    longitude = models.FloatField("longitude")
    horizontal_err = models.FloatField("horizontal_err")
    depth = models.FloatField("depth")
    depth_err = models.FloatField("depth_err")
    magnitude = models.FloatField("magnitude")
    magnitude_err = models.FloatField("magnitude_err")
    magType = models.CharField(verbose_name="Magnitude type", max_length=4)
    nst = models.IntegerField("Nst")
    magnst = models.IntegerField("Magnst")
    gap = models.IntegerField("Gap")
    dmin = models.FloatField("Dmin")
    rms = models.FloatField("Rms")
    net = models.CharField(verbose_name="Net", max_length=2)
    identifier = models.CharField(verbose_name="Identifier", max_length=20)
    place = models.CharField(verbose_name="Place", max_length=50)
    type = models.CharField(verbose_name="Type", max_length=20)
    locationSource = models.CharField(verbose_name="Location source", max_length=5, default="us")
    magSource = models.CharField(verbose_name="Magnitude source", max_length=20, default="us")
    source = models.CharField(verbose_name="Source", max_length=20, default="earthquake")

class TGF(models.Model):
    sat_source = models.CharField(verbose_name="Source", max_length=50, default="Fermi")
    TGF_name = models.CharField(verbose_name="TGF name", max_length=30)
    GEO_long = models.FloatField("Geo longitude")
    GEO_lat = models.FloatField("Geo latitude")
    trigger_time = models.DateTimeField("Trigger time")
    orbit = models.IntegerField("Orbit")
    T50 = models.TimeField("T50")
    T50_err = models.TimeField("T50 error")
    T50_err_applied = models.TimeField("T50 error applied")
    sat_altitude = models.FloatField("Satellite altitude")
    ML_counts = models.FloatField("ML counts")
    ML_counts_err = models.FloatField("ML counts error")
    ML_counts_err_applied = models.FloatField("ML counts error applied")
    event_type = models.IntegerField("Event type")
    RA = models.FloatField("RA")
    DEC = models.FloatField("DEC")
    start_time_obs = models.CharField(verbose_name="Start time observations", max_length=50)
    end_time_obs = models.CharField(verbose_name="End time observations", max_length=50)
    reliability = models.FloatField("Reliability")

class SWE(models.Model):
    sat_source = models.CharField(verbose_name="Source", max_length=50)
    flux = models.CharField(verbose_name="Flux", max_length=5)
    region = models.CharField(verbose_name="Region", max_length=20)
    trigger_time = models.CharField(verbose_name="Trigger time", max_length=50)
    time_start_obs = models.CharField(verbose_name="Time start observations", max_length=50)
    time_end_obs = models.CharField(verbose_name="Time end observations", max_length=50)
    
    def add_data():
        objs = []
        f = open("swe.csv", "r")
                    
        attributes = ["index", "flux", "region", "time_start_obs", "trigger_time", "time_end_obs"]
        next(f)
        for line in f:
            params = line.split(",")
        
            print("params:", params)
            swe = SWE()
            for att in attributes[1:]:
                print("att:", att)
                setattr(swe, att, params[attributes.index(att)])        
            objs.append(swe)
                
        return objs
            


class GRB(models.Model):
    sat_source = models.CharField(verbose_name="Source", max_length=50)
    name = models.CharField(verbose_name="Name", max_length=50)
    trigger_time = models.DateTimeField(verbose_name="Trigger time", max_length=50)
    BAT_RA = models.FloatField("RA")
    BAT_DEC = models.FloatField("DEC")
    BAT_90_err = models.FloatField("Bat 90%/ error radius")
    BAT_fluence = models.FloatField("Bat fluence")
    T90 = models.TimeField("T90 (s)")
    geo_long = models.FloatField("Geo longitude (deg)")
    geo_lat = models.FloatField("Geo latitude (deg)")
    start_time_obs = models.TimeField("Start time observations (s)")
    end_time_obs = models.TimeField("End time observations (s)")
    reliability = models.FloatField("Reliability")
    duration = models.IntegerField("Duration (s)")
    type = models.IntegerField("Type")
    sigma = models.FloatField("Sigma")
    max_count = models.IntegerField("Max count")
    BAT_fluence_90_err = models.FloatField("Fluence 90 error (kev)")
    BAT_1sec_peak_photon_flux = models.FloatField("1 sec peak photon flux")
    BAT_1sec_peak_photon_flux_90_err = models.FloatField("1 sec peak photon flux 90 err")
    BAT_photon_index = models.FloatField("Photon index")
    BAT_photon_index_90_err = models.FloatField("Photon index 90 error")
    xrtRA = models.FloatField("xrtRA")
    xrtDEC = models.FloatField("xrtDEC")
    xrt_90_err = models.FloatField("xrt 90 radius error")
    xrt_time_to_first_obs = models.CharField(verbose_name="xrt time to first observation", max_length=50)
    xrt_early_flux = models.FloatField("xrt early flux")
    xrt_11h_flux_error = models.FloatField("xrt 11 hours flux error")
    xrt_24h_flux_error = models.FloatField("xrt 24 hours flux error")
    xrt_initial_temp_index = models.FloatField("xrt initial temporal index")
    xrt_spectral_index = models.FloatField("xrt spectral index")
    xrt_column_density = models.FloatField("Column density")
    uvotRA = models.CharField(verbose_name="UVOT RA", max_length=100)
    uvotDEC = models.CharField(verbose_name="UVOT DEC", max_length=100)
    uvot_90_err = models.FloatField("UVOT 90%/ error")
    uvot_time_to_first_obs = models.CharField(verbose_name="UVOT time to first observation", max_length=100)
    uvot_magnitude = models.CharField(verbose_name="UVOT magnitude", max_length=100)
    uvot_magnitude_filter = models.CharField(verbose_name="UVOT magnitude filters", max_length=100)
    other_obs_detects = models.CharField(verbose_name="Other objects detections", max_length=100)
    redshift = models.CharField(verbose_name="Redshift", max_length=100)
    host_galaxy = models.CharField(verbose_name="Host galaxy", max_length=100)
    references = models.CharField(verbose_name="References", max_length=100)
