from django.http import HttpResponse
from django.urls import path
from .views import ProductList, say_hello, RegisterView, CustomAuthToken, AuthCheckView, ProductDetailView, ProductCreateView, OrderListView


urlpatterns = [
    path("", say_hello),
    path("products/", ProductList.as_view()),
    path("product/<int:pk>/", ProductDetailView.as_view()),
    path("product/", ProductCreateView.as_view()),
    path('hello/', AuthCheckView.as_view(), name='hello'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderListView.as_view(), name='order-create'),
]