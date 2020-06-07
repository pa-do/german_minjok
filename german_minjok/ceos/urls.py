from django.urls import path
from django.conf import settings

from . import views

app_name = "ceos"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:store_pk>/orders/', views.orders, name="orders"),
    path('order/condition/', views.set_condition, name="set_condition"),
    path('order/delete/', views.order_delete, name="order_delete"),
]
