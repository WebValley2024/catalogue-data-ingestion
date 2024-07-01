from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sampleField>/", views.sampleView, name="sampleView"),
    path("add_data/", views.add_data, name="add_data"),
    path("add_all_data/", views.add_all_data, name="add_all_data"),
    path("select_sample/", views.select_model_sample, name="select_model_sample"),
    path("select_earthquake/", views.select_earthquake, name="select_earthquake"),
    path("select_swe/", views.select_swe, name="select_swe"),
    path("select_tgf/", views.select_tgf, name="select_tgf")
]
