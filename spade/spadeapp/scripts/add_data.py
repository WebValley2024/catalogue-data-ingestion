from ..models import Earthquake, SWE, TGF, GRB

def add_earthquakes():
    objs = []
    lastindex = Earthquake.get_last_index()
    i = lastindex + 1

    with open("eq.csv", mode="r") as f:
        
        for _ in range(lastindex + 2): #must skip headers line and include last index line
            next(f)
        for line in f:
            params = line.split(",")
        
            eart = Earthquake()
            setattr(eart, 'id', i)
            for att in Earthquake.attributes:
                
                setattr(eart, att, params[Earthquake.attributes.index(att)])
            setattr(eart, "sat_source", "swe")        
            objs.append(eart)
            i += 1
    Earthquake.objects.bulk_create(objs)

def add_SWEs():
    objs = []
    lastindex = SWE.get_last_index()
    i = lastindex + 1

    with open("swe.csv", mode="r") as f:
        for _ in range(lastindex + 2): #must skip headers line and include last index line
            next(f)
        for line in f:
            params = line.split(",")
        
            swe = SWE()
            setattr(swe, 'id', i)
            for att in SWE.attributes:
                
                setattr(swe, att, params[SWE.attributes.index(att)])
            setattr(swe, "sat_source", "swe")        
            objs.append(swe)
            i += 1
    SWE.objects.bulk_create(objs)

def add_TGFs():
    objs = []
    lastindex = TGF.get_last_index()
    i = lastindex + 1

    with open("eq.csv", mode="r") as f:
        for _ in range(lastindex + 2): #must skip headers line and include last index line
            next(f)
        for line in f:
            params = line.split(",")
        
            tgf = TGF()
            setattr(tgf, 'id', i)
            for att in TGF.attributes:
                
                setattr(tgf, att, params[TGF.attributes.index(att)])
            setattr(tgf, "sat_source", "swe")        
            objs.append(tgf)
            i += 1
    TGF.objects.bulk_create(objs)

def add_GRBs():
    objs = []
    lastindex = GRB.get_last_index()
    i = lastindex + 1

    with open("eq.csv", mode="r") as f:
        for _ in range(lastindex + 2): #must skip headers line and include last index line
            next(f)
        for line in f:
            params = line.split(",")
        
            grb = GRB()
            setattr(grb, 'id', i)
            for att in GRB.attributes:
                
                setattr(grb, att, params[GRB.attributes.index(att)])
            setattr(grb, "sat_source", "swe")        
            objs.append(grb)
            i += 1
    GRB.objects.bulk_create(objs)
