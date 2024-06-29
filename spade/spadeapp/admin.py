from django.contrib import admin

from .models import SampleModel, TGF, Earthquake, SWE, GRB

# Register your models here.
admin.site.register(SampleModel)
admin.site.register(Earthquake)
admin.site.register(TGF)
admin.site.register(SWE)
admin.site.register(GRB)