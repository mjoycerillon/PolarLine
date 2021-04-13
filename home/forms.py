from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import ModelForm

from home.models import Cart


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'productId', 'quantity']