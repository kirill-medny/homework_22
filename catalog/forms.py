from django import forms
from .models import Product, Contact
from django.core.validators import ValidationError
from .constants import FORBIDDEN_WORDS

import mimetypes

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'purchase_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').lower()
        description = cleaned_data.get('description', '').lower()

        for word in FORBIDDEN_WORDS:
            if word in name:
                self.add_error('name', f"Слово '{word}' не допустимо в названии продукта.")
            if word in description:
                self.add_error('description', f"Слово '{word}' не допустимо в описании продукта.")

        return cleaned_data

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data['purchase_price']
        if purchase_price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return purchase_price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")

            # Улучшенная проверка формата файла
            mime_type = mimetypes.guess_type(image.name)[0]
            if mime_type not in ('image/jpeg', 'image/png'):
                raise ValidationError("Изображение должно быть в формате JPEG или PNG.")

        return image

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']