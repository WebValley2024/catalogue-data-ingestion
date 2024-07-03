from .models import SampleModel

def say_hello():
    SampleModel.objects.create(fieldSample='example',num='3')