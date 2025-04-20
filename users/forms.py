from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "avatar",
            "phone_number",
            "country",
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "avatar", "phone_number", "country")
