from django.urls import path
from . import views

app_name = "kakaopay"

urlpatterns = [
    path('approval/', views.approval, name="approval"),
    path('cancel/', views.cancel, name="cancel"),
    path('fail/', views.fail, name="fail"),

]