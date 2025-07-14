import uuid
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models

from django.conf import settings


class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    surname = models.CharField(max_length=255, blank=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"user: {self.email}"


class Product(models.Model):
    product_name: str = models.CharField(max_length=255)
    description: str | None = models.TextField(blank=True, default="")
    quantity: int = models.PositiveIntegerField()
    price_usd: float = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    @property
    def in_stock(self):
        return self.quantity > 0

    def __str__(self):
        return self.product_name


class Orders(models.Model):
    class Status(models.TextChoices):
        INPROCES = "InProces"
        DELIVERED = "Delivered"
        CANCELLED = "Cancelled"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.INPROCES
    )

    products = models.ManyToManyField(Product, through="OrderProducts", related_name="orders")

    def __str__(self):
        return f"Order: {self.order_id} by {self.user_id.name}"


class OrderProducts(models.Model):
    product_id: int = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    order_id: uuid = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount: int = models.IntegerField()

    @property
    def subtotal(self):
        return self.product_id.price_usd * self.amount