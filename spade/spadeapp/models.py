from django.db import models
from django.utils import timezone
from pathlib import Path

#global    

dirname = Path("/home/grp1/SpaDe/catalogue-data-ingestion/spade/spadeapp/scripts/")

# Create your models here.
class SampleModel(models.Model):
    fieldSample = models.CharField(max_length=10)
    num = models.CharField(max_length=10)

    attributes = [
        "fieldSample",
        "num",
    ]
    def __str__(self):
        return self.fieldSample
    
    def get_last_index():
        return SampleModel.objects.last().pk
    
#earthquakes table
class Earthquake(models.Model):
    trigger_time = models.DateTimeField(verbose_name="trigger_time", blank=True)
    latitude = models.FloatField(verbose_name="latitude", blank=True)
    longitude = models.FloatField(verbose_name="longitude", blank=True)
    depth = models.FloatField(verbose_name="depth", blank=True)    
    magnitude = models.FloatField(verbose_name="magnitude", max_length=50, blank=True)
    magType = models.CharField(verbose_name="Magnitude type", max_length=50, blank=True)
    nst = models.CharField(verbose_name="Nst", max_length=50, blank=True)
    gap = models.CharField(verbose_name="Gap", max_length=50, blank=True)
    dmin = models.CharField(verbose_name="Dmin", max_length=50, blank=True)
    rms = models.CharField(verbose_name="Rms", max_length=50, blank=True)
    net = models.CharField(verbose_name="Net", max_length=2, blank=True)
    identifier = models.CharField(verbose_name="Identifier", max_length=20, blank=True)
    updated = models.CharField(verbose_name="updated", max_length=20, default="", blank=True)
    place = models.CharField(verbose_name="Place", max_length=50, blank=True)
    type = models.CharField(verbose_name="Type", max_length=20, blank=True)
    horizontal_err = models.CharField(verbose_name="horizontal_err", max_length=50, blank=True)
    magnitude_err = models.CharField(verbose_name="magnitude_err", max_length=50, blank=True)
    depth_err = models.CharField(verbose_name="depth_err", max_length=50, blank=True)
    magnst = models.CharField(verbose_name="Magnst", max_length=50, blank=True)
    status = models.CharField(verbose_name="Status", max_length=50, default="", blank=True)
    locationSource = models.CharField(verbose_name="Location source", max_length=5, default="", blank=True)
    magSource = models.CharField(verbose_name="Magnitude source", max_length=20, default="", blank=True)
    sat_source = models.CharField(verbose_name="Satellite", max_length=50, blank=True)
    
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

    def get_last_index():
        return Earthquake.objects.last().pk
    
    #table update
    def add_data(delete = False):
        fileToOpen = dirname / "eq.csv"
        objs = []

        if delete:
            Earthquake.objects.all().delete()
            lastindex = 0
        else:        
            lastindex = Earthquake.get_last_index()
        
        i = lastindex + 1

        with open(fileToOpen, mode="r") as f:
            
            for _ in range(lastindex + 2): #must skip headers line and include last index line
                next(f)
            for line in f:
                params = line.split(",")
            
                eart = Earthquake()
                setattr(eart, 'id', i)
                for att in Earthquake.attributes:
                    setattr(eart, att, params[Earthquake.attributes.index(att)])
                
                objs.append(eart)
                i += 1
        Earthquake.objects.bulk_create(objs)

        
#TGF table
class TGF(models.Model):
    TGF_name = models.CharField(verbose_name="TGF name", max_length=30, blank=True)
    trigger_time = models.DateTimeField(verbose_name="Trigger time", default=timezone.now(),blank=True)
    GEO_long = models.CharField(verbose_name="Geo longitude", max_length=50,blank=True)
    GEO_lat = models.CharField(verbose_name="Geo latitude", max_length=50,blank=True)
    orbit = models.CharField(verbose_name="Orbit", max_length=50,blank=True)
    T50 = models.CharField(verbose_name="T50", max_length=50,blank=True)
    T50_err = models.CharField(verbose_name="T50 error", max_length=50,blank=True)
    T50_err_applied = models.CharField(verbose_name="T50 error applied", max_length=50,blank=True)
    sat_altitude = models.CharField(verbose_name="Satellite altitude", max_length=50,blank=True)
    ML_counts = models.CharField(verbose_name="ML counts", max_length=50,blank=True)
    ML_counts_err = models.CharField(verbose_name="ML counts error", max_length=50,blank=True)
    ML_counts_err_applied = models.CharField(verbose_name="ML counts error applied", max_length=50,blank=True)
    event_type = models.CharField(verbose_name="Event type", max_length=50, blank=True)
    normalised_duration = models.CharField(verbose_name="Normalised duration", max_length=50, default="", blank=True)
    sat_source = models.CharField(verbose_name="Source", max_length=50, default="Fermi", blank=True)
    RA = models.CharField(verbose_name="RA", max_length=50, blank=True)
    DEC = models.CharField(verbose_name="DEC", max_length=50, blank=True)
    start_time_obs = models.CharField(verbose_name="Start time observations", max_length=50, blank=True)
    end_time_obs = models.CharField(verbose_name="End time observations", max_length=50, blank=True)
    reliability = models.CharField(verbose_name="Reliability", max_length=50, blank=True)
    
    #attribute list
    attributes = [
        "TGF_name",
        "trigger_time", 
        "GEO_long", 
        "GEO_lat", 
        "orbit", 
        "T50", 
        "T50_err", 
        "T50_err_applied",
        "sat_altitude",
        "ML_counts",
        "ML_counts_err",
        "ML_counts_err_applied",
        "event_type",
        "normalised_duration",
        "sat_source",
        "RA",
        "DEC",
        "start_time_obs",
        "end_time_obs",
        "reliability"
    ]

    #methods
    def __str__(self):
        return str(self.pk)
    
    def get_last_index():
        return TGF.objects.last().pk
    
    def add_data(delete = False):
        objs = []
        fileToOpen = dirname / "tgf.csv"
        
        if delete:
            TGF.objects.all().delete()
            lastindex = 0
        else:        
            lastindex = TGF.get_last_index()
        
        i = lastindex + 1

        with open(fileToOpen, mode="r") as f:
            for _ in range(lastindex + 2): #must skip headers line and include last index line
                next(f)
            for line in f:
                params = line.split(",")
            
                tgf = TGF()
                for att in TGF.attributes:                    
                    setattr(tgf, att, params[TGF.attributes.index(att)])
                
                objs.append(tgf)
                i += 1
        TGF.objects.bulk_create(objs)

#SWE table
class SWE(models.Model):

    #fields
    flux = models.CharField(verbose_name="Flux", max_length=5, blank=True)
    region = models.CharField(verbose_name="Region", max_length=20, blank=True)
    time_start_obs = models.CharField(verbose_name="Time start observations", max_length=50, blank=True)
    trigger_time = models.DateTimeField(verbose_name="Trigger time", blank=True)
    time_end_obs = models.CharField(verbose_name="Time end observations", max_length=50, blank=True)
    sat_source = models.CharField(verbose_name="Source", max_length=50, blank=True)
    
    #attribute list
    attributes = ["top", "flux", "region", "time_start_obs", "trigger_time", "time_end_obs", "links", "sat_source"]
    
    #methods
    def __str__(self):
        return str(self.pk)
    
    def get_last_index():
        return SWE.objects.last().pk
    
    def add_data(delete = False):
        objs = []
        fileToOpen = dirname / "swe.csv"
        
        if delete:
            SWE.objects.all().delete()
            lastindex = 0
        else:        
            lastindex = SWE.get_last_index()
        
        i = lastindex + 1

        with open(fileToOpen, mode="r") as f:
            for _ in range(lastindex + 2): #must skip headers line and include last index line
                next(f)
            for line in f:
                params = line.split(",")
            
                swe = SWE()
                setattr(swe, 'id', i)
                for att in SWE.attributes:
                    if (att == 'top' or att == 'links'):
                        continue                     
                    setattr(swe, att, params[SWE.attributes.index(att)])
                
                setattr(swe, "sat_source", "swe")        
                objs.append(swe)
                i += 1
        SWE.objects.bulk_create(objs)

        

class GRB(models.Model):

    #fields
    name = models.CharField(verbose_name="Name", max_length=50, blank=True)
    trigger_time = models.DateTimeField(verbose_name="Trigger time", default=timezone.now(), blank=True)
    RA = models.CharField(verbose_name="RA", max_length=50, default="", blank=True)
    DEC = models.CharField(verbose_name="DEC", max_length=50, default="", blank=True)
    T90 = models.CharField(verbose_name="T90 (s)", max_length=50, blank=True)
    normalised_duration = models.CharField(verbose_name="normalised_duration", max_length=50, default="-", blank=True)
    sat_source = models.CharField(verbose_name="Source", max_length=50, blank=True)
    start_time_obs = models.CharField(verbose_name="Start time observations (s)", max_length=50, blank=True)
    end_time_obs = models.CharField(verbose_name="End time observations (s)", max_length=50, blank=True)
    reliability = models.CharField(verbose_name="Reliability", max_length=50, blank=True)
    geo_long = models.CharField(verbose_name="Geo longitude (deg)", max_length=50, blank=True)
    geo_lat = models.CharField(verbose_name="Geo latitude (deg)", max_length=50, blank=True)
    type = models.CharField(verbose_name="Type", max_length=50, blank=True)
    sigma = models.CharField(verbose_name="Sigma", max_length=50, blank=True)
    max_count = models.CharField(verbose_name="Max count", max_length=50, blank=True)
    BAT_RA = models.CharField(verbose_name="BAT_RA", max_length=50, blank=True)
    BAT_DEC = models.CharField(verbose_name="BAT_DEC", max_length=50, blank=True)
    BAT_T90 = models.CharField(verbose_name="BAT_T90", max_length=50, default="", blank=True)
    BAT_fluence = models.CharField(verbose_name="Bat fluence", max_length=50, blank=True)
    xrt_spectral_index = models.CharField(verbose_name="xrt spectral index", max_length=50, blank=True)
    
    #attribute list
    attributes = [
            "name",
            "trigger_time",
            "RA",
            "DEC",
            "T90",
            "normalised_duration",
            "sat_source",
            "start_time_obs",
            "end_time_obs",
            "reliability",
            "geo_long",
            "geo_lat",
            "type",
            "sigma",
            "max_count",
            "BAT_RA",
            "BAT_DEC",
            "BAT_T90",
            "BAT_fluence",
            "xrt_spectral_index",            
        ]
    
    #methods
    def __str__(self):
        return str(self.pk)
    
    def get_last_index():
        return GRB.objects.last().pk
    
    def add_data(delete = False):
        objs = []
        fileToOpen = dirname / "grb.csv"
        
        if delete:
            GRB.objects.all().delete()
            lastindex = 0
        else:        
            lastindex = GRB.get_last_index()
                
        i = lastindex + 1

        with open(fileToOpen, mode="r") as f:
            for _ in range(lastindex + 2): #must skip headers line and include last index line
                next(f)
            for line in f:
                params = line.split(",")            
                grb = GRB()
                setattr(grb, 'id', i)

                for att in GRB.attributes:                    
                    setattr(grb, att, params[GRB.attributes.index(att)])
                                        
                objs.append(grb)
                i += 1
        GRB.objects.bulk_create(objs)

class GMS(models.Model):
    #fields
    trigger_time = models.DateTimeField(verbose_name="trigger_time", default=timezone.now())
    field_magnitude_average = models.CharField(verbose_name="field_magnitude_average(nt)", blank=True, max_length=10)
    speed = models.CharField(verbose_name="speed", max_length=10, blank=True)
    source = models.CharField(verbose_name="source", max_length=10, blank=True)

    #attribute list
    attributes = [
        "trigger_time",
        "field_magnitude_average",
        "speed",
        "source"
    ]

    #methods
    def __str__(self):
        return str(self.pk)
    
    def get_last_index():
        return GMS.objects.last().pk
    
    def add_data(delete = False):
        objs = []

        if delete:
            GMS.objects.all().delete()
            lastindex = 0
        else:        
            lastindex = GMS.get_last_index()
                
        i = lastindex + 1

        fileToOpen = dirname / "gms.csv"
        
        with open(fileToOpen, mode="r") as f:
            for _ in range(lastindex + 2): #must skip headers line and include last index line
                next(f)
            for line in f:
                params = line.split(",")            
                gms = GMS()
                setattr(gms, 'id', i)

                for att in GMS.attributes:
                    setattr(gms, att, params[GMS.attributes.index(att)])    
                                        
                objs.append(gms)
                i += 1
        GMS.objects.bulk_create(objs)

    

