import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator

from .models import Store, OrderList


def is_manager(user, store):
    if store.manager == user:
        return True
    else:
        return False


def index(request):
    return render(request, 'ceos/index.html')


def orders(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    user = request.user
    if is_manager(user, store):
        orders = store.orderlist_set.all().order_by('-pk')
        paginator = Paginator(orders, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = { 'orders': page_obj }
        return render(request, 'ceos/orders.html', context)
    else:
        return redirect('main:index')


def set_condition(request):
    data = json.loads(request.body.decode('utf-8'))
    order = get_object_or_404(OrderList, pk=data['params']['order_pk'])
    print(data['params']['order_pk'])
    if is_manager(request.user, order.store):
        order_condition = data['params']['order_condition']
        order.order_condition = order_condition
        order.save()
        context = {
            'message': 'OK',
            'orderConditon': order_condition,
        }
        return JsonResponse(context)
    else:
        context = {
            'message': 'ERROR',
        }
        return JsonResponse(context)


def order_delete(request):
    data = json.loads(request.body.decode('utf-8'))
    order = get_object_or_404(OrderList, pk=data['params']['order_pk'])
    if is_manager(request.user, order.store):
        # 환불 절차를 수행하는 것이 맞다고 생각함.
        order.delete()
        context = {
            'message': 'OK',
        }
        return JsonResponse(context)
    else:
        context = {
            'message': 'ERROR',
        }
        return JsonResponse(context)

def pocket(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    user = request.user
    if is_manager(user, store):
        context = {
            'store': store,
        }
        return render(request, 'ceos/pocket.html', context)
    else:
        return redirect('main:index')

def calculator(request):
    data = json.loads(request.body.decode('utf-8'))
    store = get_object_or_404(Store, pk=data['params']['store_pk'])
    if is_manager(request.user, store):
        standard = data['params']['standard']
        year = int(data['params']['year'])
        month = int(data['params']['month'])
        day = int(data['params']['day'])
        if standard == '일별':
            start_date = datetime.datetime(year, month, day, 0, 0, 0)
            end_date = datetime.datetime(year, month, day, 23, 59, 59)
        elif standard == '월별':
            start_date = datetime.datetime(year, month, 1, 0, 0, 0)
            end_date = datetime.datetime(year, month, 31, 23, 59, 59)
        elif standard == '년도별':
            start_date = datetime.datetime(year, 1, 1, 0, 0, 0)
            end_date = datetime.datetime(year, 12, 31, 23, 59, 59)
        else:
            today = datetime.datetime.today()
            start_date = datetime.datetime(2019, 1, 1, 0, 0, 0)
            end_date = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)

        orders = list(store.orderlist_set.all().filter(order_time__range=(start_date, end_date)).values())
        context = {
            'message': 'OK',
            'orders': orders,
        }
        return JsonResponse(context)
    else:
        context = {
            'message': 'ERROR',
        }
        return JsonResponse(context)