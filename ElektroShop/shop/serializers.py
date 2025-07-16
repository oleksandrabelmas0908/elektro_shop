from rest_framework import serializers
from .models import Product, MyUser, OrderProducts, Orders


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "product_name",
            "description",
            "price_usd",
            "quantity",
        )

    def validate_price_usd(self, price):
        if price <= 0:
            raise  serializers.ValidationError(
                "Price must be more than 0"
            )
        return price


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = (
            "product_id",
            "amount",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = (
            "order_id",
            "user_id",
            "created_at",
            "status",
            "items",
        )

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must end with @example.com")
        return value