from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from reviews.models import Review

# Default Deleted Class
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='떠난 사람')[0]

def get_sentinel_store():
    return Store.objects.get_or_create(store_name='떠난 가게')[0]

# Create your models here.
class Store(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
    store_phone = models.CharField(max_length=20)
    store_number = models.CharField(max_length=20)
    store_location = models.CharField(max_length=100)
    store_cartegory = models.IntegerField(default=0, choices=[
            (0, "한식"), (1, "중국집"), (2, "일식"), (3, "피자"), (4, "치킨")
        ])
    store_image = models.ImageField(blank=True, upload_to="store/%Y/%m/%d")
    orderlists = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name="restaurant",
            through='OrderList',
        )
    reviews = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name="orderedstore",
            through='reviews.Review',
        )


class OrderList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    store = models.ForeignKey(Store, on_delete=models.SET(get_sentinel_store))
    order_condition = models.IntegerField(default=0, choices=[(0, "신청"), (1, "준비"), (2, "완료")])
    order_location =  models.CharField(max_length=100)
    order_time = models.DateTimeField(auto_now_add=True)
    order_name = models.CharField(max_length=50)
    order_price = models.IntegerField()


class StoreMenu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=50)
    menu_info = models.CharField(blank=True, max_length=50)
    menu_price = models.IntegerField()
    menu_image = models.ImageField(blank=True, upload_to="menu/%Y/%m/%d")


class PlusMenu(models.Model):
    menu = models.ForeignKey(StoreMenu, on_delete=models.CASCADE)
    plus_name = models.CharField(max_length=50)
    plus_price = models.IntegerField()