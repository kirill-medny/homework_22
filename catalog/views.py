from django.shortcuts import redirect, render

from .forms import ContactForm


def home(request):
    return render(request, "home.html")


def contacts(request):
    return render(request, "contacts.html")
