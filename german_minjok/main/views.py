from django.shortcuts import render, get_object_or_404


from ceos.models import Store
# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def menu(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    menu_list = store.storemenu_set.all()
    context = {
        'menue_list': menu_list,
        'store': store,
    }
    return render(request, 'main/menu_list.html')