from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SampleModel, TGF, SWE, Earthquake, GRB
from pathlib import Path
from datetime import datetime, timedelta
from django.core import serializers
from django.http import JsonResponse

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
    SWE.add_data()
    #Earthquake.add_data()
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

def str_to_data(s):
    try:
        date_object = datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return 0
    except TypeError:
        return 0
    return date_object

def check_dates(start_date, end_date):
    #checks
        
    #start not valid and end valid
    if start_date == 0 and end_date != 0:
        start_date = end_date - timedelta(days=30)
    #start valid and end not valid
    elif start_date != 0 and end_date == 0:
        end_date = datetime.now()
    #both not valid
    elif start_date == 0 and end_date == 0:
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
    
    #dates are swapped
    if end_date < start_date:
        tmp = start_date
        start_date = end_date 
        end_date = tmp

    return start_date, end_date

def select_earthquake(request):
    
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    
    start_date, end_date = check_dates(start_date, end_date)

    models = Earthquake.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    print("models:", models)
    
    context = {"models":models, "attributes":Earthquake.attributes}
    return render(request, "earthquake.html", context)

def select_earthquake_json(request):
        
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = Earthquake.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    return JsonResponse(data_json, safe=False)


def select_swe(request):
    
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = SWE.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')    
    context = {"models":models, "attributes":SWE.attributes}
    return render(request, "swe.html", context)

def select_swe_json(request):
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = SWE.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    return JsonResponse(data_json, safe=False)


def select_tgf(request, format = 'render'):        
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = TGF.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    context = {"models":models, "attributes":TGF.attributes}

    if format == 'render':
        return render(request, "tgf.html", context)
    if format == 'json':
        return JsonResponse(data_json, safe=False)
    
def select_tgf_json(request):
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = TGF.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    
    return JsonResponse(data_json, safe=False)


def select_grb(request, format = 'render'):
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = GRB.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    context = {"models":models, "attributes":GRB.attributes}
    if format == 'render':
        return render(request, "grb.html", context)
    if format == 'json':
        return JsonResponse(data_json, safe=False)

def select_grb_json(request):
    start_date = str_to_data(request.GET.get('start'))
    end_date = str_to_data(request.GET.get('end'))
    start_date, end_date = check_dates(start_date, end_date)

    models = GRB.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    return JsonResponse(data_json, safe=False)