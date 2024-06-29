from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SampleModel, TGF
import numpy as np

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
    
    f = open("file_ex.csv", "r") 
    objs = []
    
    for line in f:
        params = line.split(",")
        sm = SampleModel(fieldSample = params[0], num = params[1])        
        objs.append(sm)
        
    f.close()

    if objs:
        SampleModel.objects.bulk_create(objs)
    else:
        return HttpResponse("Failed")
    return HttpResponse("Data added correctly")

def sampleView(request, sampleField):
    return HttpResponse("Field is: %s." %sampleField)
