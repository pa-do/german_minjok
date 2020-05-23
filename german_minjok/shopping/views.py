from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from carton.cart import Cart
from ceos.models import StoreMenu


def menu(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    menu_list = store.storemenu_set.all()
    context = {
        'menue_list': menu_list,
        'store': store,
    }
    return render(request, 'shopping/menu_list.html')


def add_product(request):
    cart = Cart(request.session)
    menu = get_object_or_404(StoreMenu, pk=request.GET.get('menu'))
    cart.add(menu, price=menu.menu_price)
    context = {
        'total': cart.total,
    }
    return JsonResponse(context)


def minus_product(request):
    cart = Cart(request.session)
    menu = get_object_or_404(StoreMenu, pk=request.GET.get('menu'))
    cart.remove_single(menu)
    context = {
        'total': cart.total,
    }
    return JsonResponse(context)


def show_cart(request):
    return render(request, 'shopping/show_cart.html')