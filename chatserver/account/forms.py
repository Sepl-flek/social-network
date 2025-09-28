from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from account.models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Обязательное поле. Введите свой email")
    phone_number = forms.CharField(max_length=12, required=False, help_text="Необязательное поле.")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
