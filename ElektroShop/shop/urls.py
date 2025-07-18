from django.http import HttpResponse
from django.urls import path
from .views import ProductList, say_hello, RegisterView, CustomAuthToken, AuthCheckView


urlpatterns = [
    path("", say_hello),
    path("products/", ProductList.as_view()),
    path('hello/', AuthCheckView.as_view(), name='hello'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
]