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