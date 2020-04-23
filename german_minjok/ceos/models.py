from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_sentinel_store():
    return StoreInfo.objects.get_or_create(store_name='deleted')[0]


class StoreInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
    store_phone = models.CharField(max_length=20)
    store_number = models.CharField(max_length=20)
    store_location = models.CharField(max_length=100)


class StoreMenu(models.Model):
    store = models.ForeignKey(StoreInfo, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=50)
    menu_price = models.IntegerField()
    # menu_picture = models.ImageField()


class OrderList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    store = models.ForeignKey(StoreInfo, on_delete=models.SET(get_sentinel_store))
    order_condition = models.IntegerField(default=0, choices=[(0, "신청"), (1, "준비"), (2, "완료")])
    order_location =  models.CharField(max_length=100)
    order_time = models.DateTimeField(auto_now_add=True)
    order_name = models.CharField(max_length=50)
    order_price = models.IntegerField()