from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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
    # Render Home page
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
    # Retrieve the product from Product table
    product = get_object_or_404(Product, id=product_id)

    # Validate if the request's method is GET
    if request.method == 'GET':

        # Render details page passing the product details
        return render(request, 'details.html', {'product': product})
    else:
        try:
            # Retrieve the cart object passing it's composite keys user and product
            cart_item = Cart.objects.get(user=request.user.id, productId=product_id)

        except Cart.DoesNotExist:
            # If the product is not in the user's cart,
            # create a new row to add the product to user's cart
            new_cart = Cart.objects.create(user=request.user, productId=product)
            new_cart.save()

            # Redirect the user to cart page
            return redirect('cart')

        # Increment the item's quantity and save to
        # database then redirect the user to cart page
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
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

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
    # Validate if the request's method is POST
    if request.method == 'POST':

        # Validate if password and confirm password fields are the same
        if request.POST['password1'] == request.POST['password2']:

            try:
                # Create the User object with all the details from request and save/commit to database
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()

                # Calling the Django login method passing the current session and
                # the user object then redirect the current user to home page
                login(request, user)
                return redirect('home')

            # If a certain username has already been taken (Integrity Error),
            # return with HTTP Response that will render the sign up page passing the error message
            except IntegrityError:
                return render(request, 'signup.html',
                              {'form': UserForm(),
                               'error': 'Username has already been taken'})
        else:
            # Render the sign up page passing the error message
            return render(request, 'signup.html', {'form': UserForm(), 'error': 'Passwords did not match'})
    else:
        # Render the sign up page
        return render(request, 'signup.html', {'form': UserForm()})



@login_required
def account(request):
    """
    This method/will return a view of the current user's account details
    :param request: HTTP Request to render the account page
    :return: HTTP Response to render account profile and address specific for the user
    """
    # Retrieve the User Object
    user = User.objects.get(id=request.user.id)

    # Render the Account Page the user's details, profile and address
    return render(request, 'account.html', {
        'user_form': user,
        'profile_form': user.profile,
        'address_form': user.address,
    })


@login_required
def edit_profile(request):
    """
    This method/view will enable the edit profile for the user
    :param request: HTTP Request enabling the account and profile form
    :return: HTTP Response rendering the Account page
    """
    # Retrieving the user Object
    user = User.objects.get(id=request.user.id)

    # Calling the account form and profile form passing user object as instance
    user_form = AccountForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    # Render the account page passing the user and profile forms and passing user's address
    return render(request, 'account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': user.address,
    })


@login_required
def edit_address(request):
    """
    This method/view will enable the edit address for the user
    :param request: HTTP Request enabling the address form
    :return: HTTP Response rendering the Account page
    """
    # Retrieving the User Object
    user = User.objects.get(id=request.user.id)

    # Calling the address form passing User object as instance
    address_form = AddressForm(instance=request.user.address)

    # Render the account page passing the user's profile details and the address form
    return render(request, 'account.html', {
        'user_form': user,
        'profile_form': user.profile,
        'address_form': address_form,
    })


@login_required
@transaction.atomic
def profile(request):
    """
    This method/view will process the account and profile forms submitted by the user
    :param request: HTTP Request containing the details for Account and Profile forms
    :return: HTTP Response rendering the page passing an informational message for the user
    if the details has been updated or an error occurs.
    """
    # Validate if the request's method is POST
    if request.method == 'POST':

        # Calling the account form and profile form passing the details from POST
        user_form = AccountForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        # Calling the address form passing user object as instance
        address_form = AddressForm(instance=request.user.address)

        # Validate if the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save/Commit the forms to database
            user_form.save()
            profile_form.save()

            # Retrieving the updated User object and render the account page
            # with newly updated User Details
            user = User.objects.get(id=request.user.id)
            return render(request, 'account.html', {
                'user_form': user,
                'profile_form': user.profile,
                'address_form': user.address,
                'profile_message': 'Your profile was successfully updated!'
            })
        else:
            # Render the account page passing all the forms and the error message
            return render(request, 'account.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'address_form': address_form,
                'profile_error': 'Error occurred while submitting the form.'
            })
    else:
        # Redirecting to account page
        return redirect('account')


@login_required
@transaction.atomic
def address(request):
    """
    This method/view will process the address form submitted by the user
    :param request: HTTP Request containing the details for Address form
    :return: HTTP Response rendering the page passing an informational message for the user
    if the address has been updated or an error occurs.
    """
    # Validate if the request's method is POST
    if request.method == 'POST':

        # Calling the account form and Profile form passing user object as instance
        user_form = AccountForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        # Calling the address form passing the details from POST
        address_form = AddressForm(request.POST, instance=request.user.address)

        # Validate if address form is valid
        if address_form.is_valid():

            # Save/Commit the forms to database
            address_form.save()

            # Retrieving the updated user object and render the account page
            # with newly updated user address
            user = User.objects.get(id=request.user.id)
            return render(request, 'account.html', {
                'user_form': user,
                'profile_form': user.profile,
                'address_form': user.address,
                'address_message': 'Your address was successfully updated!'
            })
        else:
            # Render the account page passing all the forms and the error message
            return render(request, 'account.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'address_form': address_form,
                'address_error': 'Error occurred while submitting the form. '

            })
    else:
        # Redirecting to account page
        return redirect('account')
