from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'login_label'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'password_label'}))



class PlayerForm(forms.ModelForm):
    nickname = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'id':"nick"}))
    choice = forms.CharField(label='Your character')
    class Meta:
        model = Player
        fields = ('nickname', 'choice')
