from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import TGF, SWE, Earthquake, GRB, GMS
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from spade.forms import SignUpForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import io
import re

# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login') 
    template_name = "registration/signup.html"


def index(request):    
    template = loader.get_template("spadeapp/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: u.is_superuser)
def add_all_data(request):
    #print("Adding all data...")
    SWE.add_data()
    Earthquake.add_data()
    TGF.add_data()
    GRB.add_data()
    GMS.add_data()

    return HttpResponse("All data added")

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

def clean_data(xarr, yarr, sources):
    return zip(*[(float(x), float(y), s) for x, y, s in zip(xarr, yarr, sources) if (x not in [None, ""] and y not in [None, ""]) and (isinstance(x, float) or x != "" or "-" not in x)])

def get_svg(xarr, yarr, sources, theme):
    xarr, yarr, s_clean = clean_data(xarr, yarr, sources)
    
    # Create a figure with specified size
    plt.figure(figsize=(10, 6))  # Adjust the size as needed
    
    print(plt.style.available)
    if theme == 'dark':
        #plt.style.use('seaborn-v0_8-darkgrid')
        plt.style.use('bmh')
    else:
        plt.style.use('seaborn-v0_8-white')

    plt.subplot(111, projection='aitoff')
    plt.grid(True)
    
    # Define marker and color for each source
    colors_list = ('#0169B2', '#FFBF28', '#0169B280', '#00579480', '#FFBF2880')
    
    markers = {source: 'o' for i, source in enumerate(set(s_clean))}
    colors = {source: colors_list[i % len(colors_list)] for i, source in enumerate(set(s_clean))}
    
    # Plot each point with the corresponding marker and color
    for x, y, s in zip(xarr, yarr, s_clean):
        plt.scatter(x, y, marker=markers[s], color=colors[s], label=s)
    
    # Create a legend to avoid duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.2, 1))
    
    # Save the plot to a BytesIO object
    svg_buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    
    # Define a regular expression pattern to match width and height attributes
    pattern = r'\s(width|height)="[^"]*"'

    # Use re.sub() to remove width and height attributes from the SVG content
    svg_content = svg_buffer.getvalue().decode('utf-8') #.replace('\n', '').replace('  ', ' ')

    svg_content = re.sub(pattern, '', svg_content)
    if theme == 'dark':
        svg_content = svg_content.replace('#262626', '#f0f0f0')
        svg_content = svg_content.replace('" style="fill: #ffffff"/>', '" style="fill: none"/>')
        svg_content = svg_content.replace('#eeeeee', '#787878')
        #print("oknMLEJfe;e;FNE;nE;FNe;NEKE;n /ef;cc\n", svg_content)
    # Return the SVG content
    return f"<div>{svg_content}</div>"

def get_graph_columns(request):
    start_date, end_date = get_and_check_dates(request)
    theme = request.GET.get('theme')
    ras = list(GRB.objects.values_list('RA', flat=True).filter(trigger_time__range=(start_date, end_date))) 
    #ras = ras + list(TGF.objects.values_list('RA', flat=True).filter(trigger_time__range=(start_date, end_date)))
    decs = list(GRB.objects.values_list('DEC', flat=True).filter(trigger_time__range=(start_date, end_date)))  
    #decs = decs + list(TGF.objects.values_list('DEC', flat=True).filter(trigger_time__range=(start_date, end_date)))
    sources = list(GRB.objects.values_list('sat_source', flat=True).filter(trigger_time__range=(start_date, end_date))) 
    #sources = sources + list(TGF.objects.values_list('sat_source', flat=True).filter(trigger_time__range=(start_date, end_date)))
    svg_file = get_svg(ras, decs, sources, theme)       
    return HttpResponse(svg_file)
