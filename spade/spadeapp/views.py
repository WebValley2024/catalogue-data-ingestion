from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SampleModel, TGF, SWE, Earthquake, GRB
from pathlib import Path
from time import strftime, localtime
import json

# Create your views here.
def index(request):
    latest_fields = []
    latest_fields = SampleModel.objects.all()
    latest_field = latest_fields[0]
    template = loader.get_template("spadeapp/index.html")
    context = {
        "latest_fields": latest_fields,
        "latest_field": latest_field
    }
    return HttpResponse(template.render(context, request))

def add_data(request):
    data_folder = Path("C:/Users/Tommaso Scesi/Desktop/Challenge1/catalogue-data-ingestion/spade/spade/files_data")
    fileToOpen = data_folder / "file_ex.csv"
    f = open(fileToOpen, "r") 
    objs = []
    attributes = ["fieldSample", "num"]
    for line in f:
        #print("Line:", line)
        params = line.split(",")
        print(params)
        sm = SampleModel()
        for att in attributes:
            print("att", att)
            setattr(sm, att, params[attributes.index(att)])        
        objs.append(sm)
        
    f.close()
    print("Objs:", objs)
    if objs:
        SampleModel.objects.bulk_create(objs)
    else:
        return HttpResponse("Failed")
    return HttpResponse("Data added correctly")

def add_all_data(request):
    #SWE.add_data()
    Earthquake.add_data()
    #TGF.add_data()
    #GRB.add_data()

    return HttpResponse("All data added")

def sampleView(request, sampleField):
    return HttpResponse("Field is: %s." %sampleField)

def select_model_sample(request):
    #samplemodels = SampleModel.objects.raw("SELECT * FROM spadeapp_sampleModel")
    samplemodels = SampleModel.objects.all()    
    print(samplemodels)
    context = {"samplemodels":samplemodels}
    return render(request, "prova.html", context)

def select_earthquake(request):
    #samplemodels = SampleModel.objects.raw("SELECT * FROM spadeapp_sampleModel")
    models = Earthquake.objects.all() 
       
    #print(samplemodels)
    context = {"models":models, "attributes":Earthquake.attributes}
    return render(request, "earthquake.html", context)

def select_swe(request):
    
    models = SWE.objects.all()

    context = {"models":models, "attributes":SWE.attributes}
    return render(request, "swe.html", context)

def select_tgf(request):
    
    models = TGF.objects.all()               
    
    context = {"models":models, "attributes":TGF.attributes}
    return render(request, "tgf.html", context)

