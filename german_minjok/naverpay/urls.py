from django.urls import path
from . import views

app_name = "naverpay"

urlpatterns = [
    path('', views.index, name="index"),

]
