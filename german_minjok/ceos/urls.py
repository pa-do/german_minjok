from django.urls import path
from . import views

app_name = "ceos"

urlpatterns = [
    path('', views.index, name="index"),
]
