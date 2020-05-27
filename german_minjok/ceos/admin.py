from django.contrib import admin

from .models import Store, StoreMenu, OrderList
# Register your models here.
admin.site.register(Store)
admin.site.register(StoreMenu)
admin.site.register(OrderList)