from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    print(latest_products)  # Вывод в консоль
    return render(request, 'home.html', {'latest_products': latest_products})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        massage = request.POST.get("massage")
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, "contacts.html")


def contact(request):
    contacts = Contact.objects.all()
    return render(request, 'contact.html', {'contacts': contacts})