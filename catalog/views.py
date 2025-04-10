from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm, ContactForm
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.mail import send_mail


class HomeView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'page_obj'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.all().order_by('-created_at')[:5]
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('catalog:home')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:home')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Отправка сообщения по электронной почте
            send_mail(
                'Новое сообщение от пользователя',
                f'Имя: {name}\nEmail: {email}\nСообщение: {message}',
                'your_email@example.com',
                ['your_email@example.com'],
                fail_silently=False,
            )

            return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
        return self.render_to_response(self.get_context_data(form=form))