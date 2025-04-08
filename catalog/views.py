from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from .forms import ProductForm, ContactForm
from django.http import HttpResponse

def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3)  # 3 продукта на страницу

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Если page_number не является целым числом, вернуть первую страницу.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, вернуть последнюю страницу.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'catalog/index.html', {'page_obj': page_obj})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправьте на главную страницу после успешного создания
    else:
        form = ProductForm()
    return render(request, 'catalog/product_create.html', {'form': form})

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы (например, сохранение в БД или отправка email)
            contact = form.save()  # Сохраняем данные в модель Contact
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Здесь должна быть логика для обработки формы
            print(f"Получено сообщение от {name} ({email}): {message}")
            return HttpResponse(f"Спасибо, {name}! Сообщение получено.")  # Отправка успешного ответа
    else:
        form = ContactForm()
    return render(request, 'catalog/contacts.html', {'form': form})