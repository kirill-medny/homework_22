from urllib.request import urlopen  # Import urlopen

from django.core.files import File  # Import File class
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Adds test products to the database"

    def handle(self, *args, **kwargs):
        # Удаление существующих данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        electronics = Category.objects.create(
            name="Электроника", description="Электронные устройства"
        )
        clothing = Category.objects.create(
            name="Одежда", description="Предметы гардероба"
        )

        # Создание продуктов
        # Example with dummy image URL
        image_url = "https://loremflickr.com/640/480/product"  # Replace with actual URL
        try:
            image_file = urlopen(image_url)
            product1 = Product.objects.create(
                name="Тестовый продукт 1",
                description="Описание тестового продукта 1",
                category=electronics,
                purchase_price=100,
                image=File(image_file, name="test_product1.jpg"),
            )  # Set a filename
        except:
            product1 = Product.objects.create(
                name="Тестовый продукт 1",
                description="Описание тестового продукта 1",
                category=electronics,
                purchase_price=100,
            )

        product2 = Product.objects.create(
            name="Тестовый продукт 2",
            description="Описание тестового продукта 2",
            category=clothing,
            purchase_price=50,
        )

        self.stdout.write(self.style.SUCCESS("Successfully added test products"))
