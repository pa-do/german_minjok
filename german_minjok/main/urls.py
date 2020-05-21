from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:store_pk>/menu/', views.menu, name="menu"),
]