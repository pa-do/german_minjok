from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('division/', views.signup_div, name='div'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:phone_num>/', views.phone, name='phone'),
    path('<str:phone_num>/<str:auth_num>/', views.phone_auth, name='phone_auth'),

]