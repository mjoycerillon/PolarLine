from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'index.html')


def shop(request):
    return render(request, 'shop.html')


def contactus(request):
    return render(request, 'contactus.html')


def login(request):
    return render(request, 'login.html')


def cart(request):
    return render(request, 'cart.html')
