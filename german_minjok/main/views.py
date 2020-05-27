from django.shortcuts import render

from ceos.models import Store

# Create your views here.
def index(request):

    return render(request, 'main/index.html')

def temp(request, category):
    if category != 5:
        stores = Store.objects.filter(store_cartegory=category)
    else:
        stores = Store.objects.all()
    context = {
        'category': category,
        'stores': stores,
    }
    return render(request, 'main/temp.html', context)