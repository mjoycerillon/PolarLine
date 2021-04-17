from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, Address


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'birth_date')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('shipping_address', 'billing_address')


class ContactForm(forms.Form):
    from_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'What\'s this about?'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Go ahead we\'re listening...'}))


