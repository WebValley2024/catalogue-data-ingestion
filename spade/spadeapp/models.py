from django.db import models
from django.utils import timezone
from pathlib import Path

#global
data_folder = Path("C:/Users/Tommaso Scesi/Desktop/Challenge1/catalogue-data-ingestion/spade/spade/files_data")
    

# Create your models here.
class SampleModel(models.Model):
    fieldSample = models.CharField(max_length=10)
    num = models.CharField(max_length=10)

    def __str__(self):
        return self.fieldSample
    
class Earthquake(models.Model):
    trigger_time = models.CharField(verbose_name="trigger_time", max_length=50)
    latitude = models.FloatField(verbose_name="latitude")
    longitude = models.FloatField(verbose_name="longitude")
    depth = models.FloatField(verbose_name="depth")    
    magnitude = models.FloatField(verbose_name="magnitude", max_length=50)
    magType = models.CharField(verbose_name="Magnitude type", max_length=50)
    nst = models.CharField(verbose_name="Nst", max_length=50)
    gap = models.CharField(verbose_name="Gap", max_length=50)
    dmin = models.CharField(verbose_name="Dmin", max_length=50)
    rms = models.CharField(verbose_name="Rms", max_length=50)
    net = models.CharField(verbose_name="Net", max_length=2)
    identifier = models.CharField(verbose_name="Identifier", max_length=20)
    updated = models.CharField(verbose_name="updated", max_length=20, default="loaded")
    place = models.CharField(verbose_name="Place", max_length=50)
    type = models.CharField(verbose_name="Type", max_length=20)
    horizontal_err = models.CharField(verbose_name="horizontal_err", max_length=50)
    magnitude_err = models.CharField(verbose_name="magnitude_err", max_length=50)
    depth_err = models.CharField(verbose_name="depth_err", max_length=50)
    magnst = models.CharField(verbose_name="Magnst", max_length=50)
    status = models.CharField(verbose_name="Status", max_length=50, default="0")
    locationSource = models.CharField(verbose_name="Location source", max_length=5, default="us")
    magSource = models.CharField(verbose_name="Magnitude source", max_length=20, default="us")
    sat_source = models.CharField(verbose_name="Satellite", max_length=50)
    
    attributes = [
            "trigger_time", 
            "latitude", 
            "longitude", 
            "depth", 
            "magnitude", 
            "magType", 
            "nst",
            "gap",
            "dmin",
            "rms",
            "net",
            "identifier",
            "updated",
            "place",
            "type",
            "horizontal_err",
            "depth_err",
            "magnitude_err",
            "magnst",
            "status",            
            "locationSource",
            "magSource",
            "sat_source"            
        ]
    
    def __str__(self):
        return str(self.pk)    

    def add_data():
        objs = []
        fileToOpen = data_folder / "earthquake.csv"
        f = open(file=fileToOpen, mode="r", encoding="cp850")
                   
        
        next(f)
        for line in f:
            params = line.split(",")
                    
            eart = Earthquake()
            for att in Earthquake.attributes:                
                setattr(eart, att, params[Earthquake.attributes.index(att)])        
            objs.append(eart)

        if objs:
            Earthquake.objects.all().delete()
            Earthquake.objects.bulk_create(objs)    
        

class TGF(models.Model):
    GEO_long = models.CharField(verbose_name="Geo longitude", max_length=50)
    GEO_lat = models.CharField(verbose_name="Geo latitude", max_length=50)
    orbit = models.CharField(verbose_name="Orbit", max_length=50)
    trigger_time = models.DateTimeField(verbose_name="Trigger time", default=timezone.now())
    T50 = models.CharField(verbose_name="T50", max_length=50)
    T50_err = models.CharField(verbose_name="T50 error", max_length=50)
    T50_err_applied = models.CharField(verbose_name="T50 error applied", max_length=50)
    sat_altitude = models.CharField(verbose_name="Satellite altitude", max_length=50)
    ML_counts = models.CharField(verbose_name="ML counts", max_length=50)
    ML_counts_err = models.CharField(verbose_name="ML counts error", max_length=50)
    ML_counts_err_applied = models.CharField(verbose_name="ML counts error applied", max_length=50)
    TGF_name = models.CharField(verbose_name="TGF name", max_length=30)
    event_type = models.CharField(verbose_name="Event type", max_length=50)
    normalised_duration = models.CharField(verbose_name="Normalised duration", max_length=50, default="1")
    sat_source = models.CharField(verbose_name="Source", max_length=50, default="Fermi")
    RA = models.CharField(verbose_name="RA", max_length=50)
    DEC = models.CharField(verbose_name="DEC", max_length=50)
    start_time_obs = models.CharField(verbose_name="Start time observations", max_length=50)
    end_time_obs = models.CharField(verbose_name="End time observations", max_length=50)
    reliability = models.CharField(verbose_name="Reliability", max_length=50)
    
    attributes = [
        "GEO_long", 
        "GEO_lat", 
        "orbit", 
        "trigger_time", 
        "T50", 
        "T50_err", 
        "T50_err_applied",
        "sat_altitude",
        "ML_counts",
        "ML_counts_err",
        "ML_counts_err_applied",
        "TGF_name",
        "event_type",
        "normalised_duration",
        "sat_source",
        "RA",
        "DEC",
        "start_time_obs",
        "end_time_obs",
        "reliability"
    ]

    def __str__(self):
        return str(self.pk)
    
    def add_data():
        objs = []
        fileToOpen = data_folder / "tgf.csv"
        f = open(fileToOpen, "r")
                    
        
        next(f)
        for line in f:
            params = line.split(",")
                    
            tgf = TGF()
            for att in TGF.attributes:
                if (att == "reliability" and params[TGF.attributes.index(att)] == '\n'):
                    setattr(tgf, att, "-")
                setattr(tgf, att, params[TGF.attributes.index(att)])        
            objs.append(tgf)

        if objs:
            TGF.objects.all().delete()
            TGF.objects.bulk_create(objs)    
    

class SWE(models.Model):
    flux = models.CharField(verbose_name="Flux", max_length=5)
    region = models.CharField(verbose_name="Region", max_length=20)
    trigger_time = models.CharField(verbose_name="Trigger time", max_length=50)
    time_start_obs = models.CharField(verbose_name="Time start observations", max_length=50)
    time_end_obs = models.CharField(verbose_name="Time end observations", max_length=50)
    sat_source = models.CharField(verbose_name="Source", max_length=50)
    
    attributes = ["flux", "region", "time_start_obs", "trigger_time", "time_end_obs", "sat_source"]
        
    def __str__(self):
        return str(self.pk)
    
    def add_data():
        objs = []
        fileToOpen = data_folder / "swe.csv"    
        f = open(fileToOpen, "r")
                    
        next(f)
        for line in f:
            params = line.split(",")
        
            print("params:", params)
            swe = SWE()
            for att in SWE.attributes[:-1]:
                setattr(swe, att, params[SWE.attributes.index(att)])
            setattr(swe, "sat_source", "swe")        
            objs.append(swe)

        if objs:
            SWE.objects.all().delete()
            SWE.objects.bulk_create(objs)    
        

class GRB(models.Model):
    trigger_time = models.DateTimeField(verbose_name="Trigger time", default=timezone.now())
    BAT_RA = models.FloatField("BAT_RA")
    BAT_DEC = models.FloatField("BAT_DEC")
    BAT_90_err = models.FloatField("Bat 90%/ error radius")
    BAT_fluence = models.FloatField("Bat fluence")
    T90 = models.TimeField("T90 (s)")
    sat_source = models.CharField(verbose_name="Source", max_length=50)
    RA = models.CharField(verbose_name="RA", max_length=50, default="0")
    DEC = models.CharField(verbose_name="DEC", max_length=50, default="0")
    name = models.CharField(verbose_name="Name", max_length=50)
    geo_long = models.FloatField("Geo longitude (deg)")
    geo_lat = models.FloatField("Geo latitude (deg)")
    start_time_obs = models.DateTimeField(verbose_name="Start time observations (s)", default=timezone.now())
    end_time_obs = models.DateTimeField(verbose_name="End time observations (s)", default=timezone.now())
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
    xrt_time_to_first_obs = models.TimeField(verbose_name="xrt time to first observation", max_length=50)
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

    def __str__(self):
        return str(self.pk)
    
    def add_data():
        objs = []
        fileToOpen = data_folder / "grb.csv"    
        f = open(fileToOpen, "r")
                    
        attributes = [
            "name",
            "trigger_time",
            "BAT_ra",
            "BAT_dec",
            "BAT_90_err",
            "BAT_fluence",
            "T90",    
            "source",
            "RA",
            "DEC",                    
            "geo_long",
            "geo_lat",
            "start_time_obs",
            "end_time_obs",
            "reliability",
            "duration",
            "type",
            "sigma",
            "max_count",
            "BAT_fluence_90_err",
            "BAT_1sec_peak_photon_flux",
            "BAT_1sec_peak_photon_flux_90_err",
            "BAT_photon_index",
            "BAT_photon_index_90_err",
            "xrtRA",
            "xrtDEC",
            "xrt_90_err",
            "xrt_time_to_first_obs",
            "xrt_early_flux",
            "xrt_11h_flux_error",
            "xrt_24h_flux_error",
            "xrt_initial_temp_index",
            "xrt_spectral_index",
            "xrt_column_density",
            "uvotRA",
            "uvotDEC",
            "uvot_90_err",
            "uvot_time_to_first_obs",
            "uvot_magnitude",
            "uvot_magnitude_filter",
            "other_obs_detects",
            "redshift",
            "host_galaxy",
            "references"            
        ]
        next(f)
        for line in f:
            params = line.split(",")
        
            grb = GRB()
            
            for att in attributes:
                setattr(grb, att, params[attributes.index(att)])   
                 
            objs.append(grb)

        if objs:
            SWE.objects.bulk_create(objs)    
        
