from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request, 'main/index.html')

def temp(request):

    return render(request, 'main/temp.html')