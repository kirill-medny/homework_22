from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ContactsView, HomeView, ProductCreateView,
                           ProductDeleteView, ProductDetailView,
                           ProductUpdateView, product_list,
                           products_by_category)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "category/<str:category_name>/",
        products_by_category,
        name="products_by_category",
    ),
    path("products/", product_list, name="product_list"),
]
