import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from dotenv import load_dotenv

from .forms import (CustomAuthenticationForm, CustomUserChangeForm,
                    UserRegisterForm)

load_dotenv(override=True)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                subject="Добро пожаловать!",
                message="Спасибо за регистрацию на нашем сайте.",
                from_email=os.getenv("EMAIL_HOST_USER"),  # Ваш email
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect("catalog:home")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": form})
