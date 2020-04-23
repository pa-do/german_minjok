from django.db import models
from django.conf import settings

# Create your models here.

class StoreInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
    store_phone = models.CharField(max_length=20)
    store_number = models.CharField(max_length=20)
    store_location = models.CharField(max_length=100)


class StoreMenu(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(StoreInfo, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=50)
    menu_price = models.IntegerField()
    # menu_picture = models.ImageField()


class OrderList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(StoreInfo, on_delete=models.CASCADE)
    menu = models.ForeignKey(StoreMenu, on_delete=models.CASCADE)
    order_status = models.IntegerField()