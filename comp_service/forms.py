from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control required'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control required'}))


class ContactForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-group'}))
    name = forms.CharField(label='Имя', required=True)
    mess = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)
