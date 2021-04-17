from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import UserForm, ProfileForm, AccountForm, AddressForm, ContactForm
from .models import Cart, Product


def home(request):
    """
    This view will handle the rendering of Home Page
    :param request: HTTP Request - Main Page
    :return: HTTP Response - index.html
    """
    return render(request, 'index.html')


def shop(request):
    """
    This view will handle the rendering of shop page
    to display all the available products in the db
    :param request: HTTP Request - Main Page
    :return: HTTP Response - shop.html
    """
    # Retrieve all the products from the Product table
    product = Product.objects.all()
    # Render the Shop Page passing all the products
    return render(request, 'shop.html', {'product': product})


def details(request, product_id):
    """
    This view will handle the rendering of details page
    to display the details of a product
    :param request: HTTP Request - Shop Page
    :param product_id: Unique Identifier of each product in Product Model Table in sqlite db
    :return: HTTP Response - details.html
    """
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
                cart_item.quantity += 1
                cart_item.save() 
                return redirect('cart')


def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@polarline.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contactus.html", {'form': form})


def contact_success(request):
    return HttpResponse('Success! Thank you for your message.')


@login_required
def logout_user(request):
    """
    This method/view will log out the current user
    :param request: HTTP Request - current session
    :return: HTTP Response to log out the current user and
    redirect to home page
    """
    # Validate if the request's method is POST
    if request.method == 'POST':
        # Calling the Django logout method passing the current session and
        # the user object then redirect the current user to home page
        logout(request)
        return redirect('home')


def login_user(request):
    """
    This method/view will let a user log in to Polar Line
    :param request: HTTP Request to view login the login page
    :return: HTTP Response to render the login page if an error occurs
    else redirect to home page
    """
    # Validate if the request's method is POST
    if request.method == 'POST':
        # Call the Django authenticate method to retrieve the user object based on the
        # username and password submitted by the user
        user = authenticate(request, username=request.POST['username']
                            , password=request.POST['password'])
        # Validate if user is not found
        if user is None:
            # Render the login page, passing the authentication form and the error message
            return render(request,
                          'login.html',
                          {'form': AuthenticationForm(),
                           'error': 'Username or password you entered is incorrect.'})
        else:
            # Calling the Django login method passing the current session and
            # the user object then redirect the current user to home page
            login(request, user)
            return redirect('home')
    else:
        # Render the login page passing the Authentication form
        return render(request, 'login.html', {'form': AuthenticationForm()})


def cart(request):
    """
    This method/view will get all of the cart items
    that is related to the current user
    :param request: HTTP GET Request to view Cart page
    :return: HTTP Response to render the Cart page passing
    all of the cart items related to current user
    """
    userCart = None
    # Validate if the user is logged on
    if request.user.is_authenticated:
        # Retrieve all the carts related to user
        userCart = Cart.objects.filter(user=request.user)
    else:
        # Set to an empty cart
        userCart = []

    # Validate if the request's method is GET
    if request.method == 'GET':
        # Render the Cart page passing the list of cart items
        return render(request, 'cart.html', {'cart': userCart})


def remove_item(request, cart_id):
    """
    This method/view will remove a specific item from the cart
    :param request: HTTP Request containing the current session
    :param cart_id: Cart ID
    :return: HTTP Response redirecting to the Cart Page
    """
    # Retrieve the cart item from Cart table
    cart_item = get_object_or_404(Cart, id=cart_id)
    # Validate if the request's method is POST
    if request.method == 'POST':
        # Delete the cart object from the Cart Table
        # and redirect the user to cart page
        cart_item.delete()
        return redirect('cart')


def increment_item(request, cart_id):
    """
    This method/view will increment the quantity of a specific item in the cart
    :param request: HTTP Request containing the current session
    :param cart_id: Cart ID
    :return: HTTP Response redirecting to the Cart Page
    """
    # Retrieve the cart item from Cart table
    cart_item = get_object_or_404(Cart, id=cart_id)
    # Validate if the request's method is POST
    if request.method == 'POST':
        # Increment the quantity and save the changes to the object
        # then redirect the user to cart page
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')


def decrement_item(request, cart_id):
    """
    This method/view will decrement the quantity of a specific item in the cart
    :param request: HTTP Request containing the current session
    :param cart_id: Cart ID
    :return: HTTP Response redirecting to the Cart Page
    """
    # Retrieve the cart item from Cart table
    cart_item = get_object_or_404(Cart, id=cart_id)
    # Validate if the request's method is POST
    if request.method == 'POST':
        # Validate if the current quantity is greater than zero
        if cart_item.quantity > 0:
            # Decrement the quantity and save the changes to the object
            # then redirect the user to cart page
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')


def signup_user(request):
    """
    This method/view will let a user sign in i.e create an account to Polar Line
    :param request: HTTP Request to view signup page
    :return: HTTP Response to render the signup page if an error occurs
    else redirect to home page
    """
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
