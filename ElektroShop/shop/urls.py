from django.http import HttpResponse
from django.urls import path
from .views import ProductList, say_hello

urlpatterns = [
    path("", say_hello),
    path("products/", ProductList.as_view()),
]