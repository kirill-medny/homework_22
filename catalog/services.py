from .models import Product


def get_products_by_category(category_name):
    return Product.objects.filter(category=category_name)
