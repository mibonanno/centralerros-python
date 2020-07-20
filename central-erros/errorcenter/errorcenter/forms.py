from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=254, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

