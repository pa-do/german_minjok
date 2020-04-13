from django.urls import path
from . import views

app_name = "kakaopay"

urlpatterns = [
    path('', views.index, name="index"),

]
