from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "ceos"

urlpatterns = [
    path('', views.index, name="index"),
    path('create_store/', views.create_store, name="create_store"),
    path('update_store/<int:store_pk>/', views.update_store, name="update_store"),
    path('detail_store/<int:store_pk>/', views.detail_store, name='detail_store'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
