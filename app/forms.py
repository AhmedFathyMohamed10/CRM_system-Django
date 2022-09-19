from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class UserForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=11, required=True)
    address = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['name', 'phone', 'address', 'username', 'email', 'password1', 'password2']



