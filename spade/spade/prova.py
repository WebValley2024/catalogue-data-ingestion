
from spade.spadeapp.models import SampleModel

def add_sample():
    objs = []
    lastindex = SampleModel.get_last_index()
    i = lastindex + 1

    with open("file_ex.csv", mode="r") as f:
        for _ in range(lastindex + 2): #must skip headers line and include last index line
            next(f)
        for line in f:
            params = line.split(",")
        
            sm = SampleModel()
            setattr(sm, 'id', i)
            for att in SampleModel.attributes:
                
                setattr(sm, att, params[SampleModel.attributes.index(att)])
            setattr(sm, "sat_source", "swe")        
            objs.append(sm)
            i += 1
    SampleModel.objects.bulk_create(objs)

add_sample()