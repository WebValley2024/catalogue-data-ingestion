from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sampleField>/", views.sampleView, name="sampleView"),
    path("add_data/", views.add_data, name="add_data"),
    path("add_all_data/", views.add_all_data, name="add_all_data")
]