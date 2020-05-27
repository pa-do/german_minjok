from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup_div, name='div'),
    path('consumer/', views.consumer, name='consumer'),
    path('manager/', views.manager, name='manager'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:phone_num>/', views.phone, name='phone'),
    path('<str:phone_num>/<str:auth_num>/', views.phone_auth, name='phone_auth'),

]