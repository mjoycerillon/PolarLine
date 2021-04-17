from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, Address


class UserForm(UserCreationForm):
    """ This class is a form for creating Users """
    class Meta:
        """ This class contains the fields that will be available in the form """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AccountForm(forms.ModelForm):
    """ This class is a form for updating User table """
    class Meta:
        """ This class contains the fields that will be available in the form """
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    """ This class is a form for updating Profile table """
    class Meta:
        """ This class contains the fields that will be available in the form """
        model = Profile
        fields = ('phone', 'birth_date')


class AddressForm(forms.ModelForm):
    """ This class is a form for updating Address table """
    class Meta:
        """ This class contains the fields that will be available in the form """
        model = Address
        fields = ('shipping_address', 'billing_address')


class ContactForm(forms.Form):
    """ This class is a form for Contact Us page """
    from_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email'}))
    subject = forms.CharField(required=True, widget=forms.TextInput
    (attrs={'placeholder': 'What\'s this about?'}))
    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder': 'Go ahead we\'re listening...'}))


