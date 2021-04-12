from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect


# Create your views here.
from home.forms import UserForm


def home(request):
    return render(request, 'index.html')


def shop(request):
    return render(request, 'shop.html')


def contactus(request):
    return render(request, 'contactus.html')


def loginuser(request):
    return render(request, 'login.html')


def cart(request):
    return render(request, 'cart.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html',
                              {'form': UserCreationForm(), 'error': 'Username has already been taken'})
        else:
            # Password didn't match
            return render(request, 'signup.html', {'form': UserForm(), 'error': 'Passwords did not match'})

