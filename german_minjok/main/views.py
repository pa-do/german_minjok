from django.shortcuts import render, get_object_or_404
from accounts.models import *
from ceos.models import Store


def index(request):
    if request.user.is_authenticated:
        location = UserLocation.objects.get(user=request.user)
        context = {
            'adr': location.location_basic,
            'dadr': location.location_detail,
        }
    else:
        context = {

        }
    return render(request, 'main/index.html', context)


def stores(request, category):
    if category != 5:
        stores = Store.objects.filter(store_cartegory=category)
    else:
        stores = Store.objects.all()

    category_name = ['한식', '중식', '일식', '피자', '치킨', '전체']

    context = {
        'category': category,
        'stores': stores,
        'store_name': category_name[category],
    }
    return render(request, 'main/stores.html', context)


def menu(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    menu_list = store.storemenu_set.all()
    print(store, menu_list)
    context = {
        'menu_list': menu_list,
        'store': store,
    }
    return render(request, 'main/menu_list.html', context)