from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import *
from ceos.models import Store

from ceos.forms import StoreForm

# Create your views here.
@login_required
def index(request):
    if request.user.auth_code == 2:
        stores = Store.objects.filter(manager=request.user)
        context = {
            'stores': stores,
        }
        return render(request, 'ceos/index.html', context)
    else:
        return redirect('main:index')


@login_required
def create_store(request):
    if request.user.auth_code == 2:
        store_form = StoreForm(request.POST, request.FILES)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.manager = request.user
            store.save()
            return redirect('ceos:index')
        else:
            store_form = StoreForm()
        context = {
            'store_form': store_form,
        }
        return render(request, 'ceos/form_store.html', context)
    else:
        return redirect('main:index')


@login_required
def update_store(request, store_pk):
    if request.user.auth_code == 2:
        store = get_object_or_404(Store, pk=store_pk)
        if request.user == store.manager:
            store_form = StoreForm(request.POST, instance=store)
            if store_form.is_valid():
                store = store_form.save(commit=False)
                store.manager = request.user
                store.save()
                return redirect('ceos:index')
            else:
                store_form = StoreForm(instance=store)
            context = {
                'store_form': store_form,
            }
            return render(request, 'ceos/form_store.html', context)
        else:
            return redirect('ceos:index')
    else:
        return redirect('main:index')


@login_required
def detail_store(request, store_pk):
    if request.user.auth_code == 2:
        store = get_object_or_404(Store, pk=store_pk)
        if request.user == store.manager:
            menu_list = store.storemenu_set.all()
            context = {
                'store': store,
                'menu_list': menu_list,
            }
            return render(request, 'ceos/detail_store.html', context)
        else:
            return redirect('ceos:index')
    else:
        return redirect('main:index')