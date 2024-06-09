from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Ім`я користувача'}),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),

    )
    class Meta:
        fields = ['username', 'password']

class SearchForm(forms.Form):
    class_name = forms.CharField(label='Клас', max_length=100, required=False)
    teacher_name = forms.CharField(label='Вчитель', max_length=100, required=False)