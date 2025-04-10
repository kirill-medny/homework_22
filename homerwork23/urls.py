from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
