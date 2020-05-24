from django.urls import path

from . import views

app_name = 'shopping'
urlpatterns = [
    path('<int:store_pk>/menu/', views.menu, name='menu'),
    path('add/', views.add_product, name='add_product'),
    path('minus/', views.minus_product, name='minus_product'),
    path('show/', views.show_cart, name='show_cart'),
]