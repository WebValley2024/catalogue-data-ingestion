from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SampleModel

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

def sampleView(request, sampleField):
    return HttpResponse("Field is: %s." %sampleField)
