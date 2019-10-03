from django import forms
from django.contrib.auth.forms import  UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Имя',
            'password1':'Пароль',
            'password2':'Пароль повтор'
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar')


class CustomTestUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',)