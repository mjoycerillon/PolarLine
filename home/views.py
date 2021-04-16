from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from home.forms import UserForm, ProfileForm, AccountForm, AddressForm
from home.models import Cart, Product, Profile


def home(request):
    return render(request, 'index.html')


def shop(request):
    product = Product.objects.all()
    return render(request, 'shop.html',{'product':product})


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(user=request.user.id, productId=product_id)
    except Cart.DoesNotExist:
        cart = None

    if request.method == 'GET':
        return render(request, 'details.html', {'product': product})
    else:
        if cart is None:
            newCart = Cart.objects.create(user=request.user, productId=product)
            newCart.save()
            return redirect('cart')
        else:
            cart_item = get_object_or_404(Cart, id=cart.id)
            if request.method == 'POST':
                cart_item.save()
                return redirect('cart')

    

def contactus(request):
    return render(request, 'contactus.html')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username']
                            , password=request.POST['password'])
        if user is None:
            return render(request,
                          'login.html',
                          {'form': AuthenticationForm(),
                           'error': 'Username or password you entered is incorrect.'})
        else:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'login.html', {'form': AuthenticationForm()})


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
    else:
        cart = []
    if request.method == 'GET':
        return render(request, 'cart.html', {'cart': cart})


def remove_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('cart')


def increment_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')


def decrement_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        if cart_item.quantity > 0:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')


def signup_user(request):
    if request.method == 'POST':
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
    else:
        return render(request, 'signup.html', {'form': UserForm()})


@login_required
def account(request):
    user = User.objects.get(id=request.user.id)

    return render(request, 'account.html', {
        'user_form': user,
        'profile_form': user.profile,
        'address_form': user.address,
    })


@login_required
def edit_profile(request):
    user = User.objects.get(id=request.user.id)
    user_form = AccountForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': user.address,
    })


@login_required
def edit_address(request):
    user = User.objects.get(id=request.user.id)
    address_form = AddressForm(instance=request.user.address)

    return render(request, 'account.html', {
        'user_form': user,
        'profile_form': user.profile,
        'address_form': address_form,
    })


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = AccountForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        address_form = AddressForm(instance=request.user.address)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            user = User.objects.get(id=request.user.id)
            return render(request, 'account.html', {
                'user_form': user,
                'profile_form': user.profile,
                'address_form': user.address,
                'profile_message': 'Your profile was successfully updated!'
            })
        else:
            return render(request, 'account.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'address_form': address_form,
                'profile_error': 'Error occurred while submitting the form. '
            })
    else:
        user_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        address_form = AddressForm(instance=request.user.address)

    return render(request, 'account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
    })


@login_required
@transaction.atomic
def address(request):
    if request.method == 'POST':
        user_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        address_form = AddressForm(request.POST, instance=request.user.address)

        if address_form.is_valid():
            address_form.save()
            user = User.objects.get(id=request.user.id)
            return render(request, 'account.html', {
                'user_form': user,
                'profile_form': user.profile,
                'address_form': user.address,
                'address_message': 'Your address was successfully updated!'
            })
        else:
            return render(request, 'account.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'address_form': address_form,
                'address_error': 'Error occurred while submitting the form. '

            })
    else:
        user_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        address_form = AddressForm(instance=request.user.address)

    return render(request, 'account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
    })
