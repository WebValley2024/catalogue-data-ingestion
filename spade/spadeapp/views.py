from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SampleModel, TGF, SWE
import inspect

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
    objs_swe = SWE.add_data()
    if objs_swe:
        SWE.objects.bulk_create(objs_swe)
    else:
        return HttpResponse("Failed")
    return HttpResponse("Data added correctly")


def sampleView(request, sampleField):
    return HttpResponse("Field is: %s." %sampleField)
