from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sampleField>/", views.sampleView, name="sampleView")
]