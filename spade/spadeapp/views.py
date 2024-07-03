from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import TGF, SWE, Earthquake, GRB, GMS
from django.core import serializers
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView
from datetime import datetime, timedelta

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 
    template_name = "registration/signup.html"


def index(request):    
    template = loader.get_template("spadeapp/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: u.is_superuser)
def add_all_data(request):
    #print("TEST PASSED")
    SWE.add_data()
    Earthquake.add_data()
    TGF.add_data()
    GRB.add_data()
    GMS.add_data()

    return HttpResponse("All data added")

def sampleView(request, sampleField):
    return HttpResponse("Field is: %s." %sampleField)

def str_to_data(s):
    try:
        date_object = datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return 0
    except TypeError:
        return 0
    return date_object

def get_and_check_dates(request, p1 = 'start', p2 = 'end'):

    start_date = str_to_data(request.GET.get(p1))
    end_date = str_to_data(request.GET.get(p2))

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


def get_date(request, p1, p2):
    start_date = request.GET.get(p1)
    end_date = request.GET.get(p2)

    return start_date, end_date

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
    start_date, end_date = get_and_check_dates(request)
    models = Earthquake.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    context = {"models":models, "attributes":Earthquake.attributes}
    return render(request, "earthquake.html", context)

def select_earthquake_json(request):    
    start_date, end_date = get_and_check_dates(request)
    models = Earthquake.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    return HttpResponse(data_json, content_type='application/json')

def select_swe(request):    
    start_date, end_date = get_and_check_dates(request)
    models = SWE.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')    
    context = {"models":models, "attributes":SWE.attributes}
    return render(request, "swe.html", context)

def select_swe_json(request):
    start_date, end_date = get_and_check_dates(request)
    models = SWE.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    return HttpResponse(data_json, content_type='application/json')

def select_tgf(request):        
    start_date, end_date = get_and_check_dates(request)
    models = TGF.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    context = {"models":models, "attributes":TGF.attributes}
    return render(request, "tgf.html", context)
    
def select_tgf_json(request):
    start_date, end_date = get_and_check_dates(request)
    models = TGF.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)    
    return HttpResponse(data_json, content_type='application/json')
    

def select_grb(request):
    start_date, end_date = get_and_check_dates(request)
    models = GRB.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    context = {"models":models, "attributes":GRB.attributes}    
    return render(request, "grb.html", context)
    

def select_grb_json(request):
    start_date, end_date = get_and_check_dates(request)
    models = GRB.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)
    return HttpResponse(data_json, content_type='application/json')
    

def select_gms(request):
    start_date, end_date = get_and_check_dates(request)
    models = GMS.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    context = {"models":models, "attributes":GMS.attributes}    
    return render(request, "gms.html", context)
    
def select_gms_json(request):
    start_date, end_date = get_and_check_dates(request)
    models = GMS.objects.filter(trigger_time__range=(start_date, end_date)).order_by('-trigger_time')
    data_json = serializers.serialize('json', models)    
    return HttpResponse(data_json, content_type='application/json')