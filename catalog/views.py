from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import ContactForm, ProductForm
from .models import Product
from .services import get_products_by_category


class HomeView(ListView):
    model = Product
    template_name = "catalog/index.html"
    context_object_name = "page_obj"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.all().order_by("-created_at")[:5]
        return context


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.can_unpublish_product"
        )


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.delete_product"
        )


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Отправка сообщения по электронной почте
            send_mail(
                "Новое сообщение от пользователя",
                f"Имя: {name}\nEmail: {email}\nСообщение: {message}",
                "your_email@example.com",
                ["your_email@example.com"],
                fail_silently=False,
            )

            return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
        return self.render_to_response(self.get_context_data(form=form))


def products_by_category(request, category_name):
    products = get_products_by_category(category_name)
    return render(
        request,
        "catalog/products_by_category.html",
        {"products": products, "category_name": category_name},
    )


def product_list(request):
    cache_key = "product_list"
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.all()
        cache.set(cache_key, products, timeout=60 * 15)  # Кеширование на 15 минут

    return render(request, "catalog/product_list.html", {"products": products})
