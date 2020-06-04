from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:category>/stores', views.stores, name="stores"),
    path('<int:store_pk>/menu/', views.menu, name='menu'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
