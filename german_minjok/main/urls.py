from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:store_pk>/menu/', views.menu, name="menu"),
    path('')
    path('<int:store_pk>/<int:menu_pk>/add/', views.add_cart, name="add_cart"),
    path('<int:store_pk>/int:menu_pk>/remove/', views.remove_cart, name="remove_cart"),
]