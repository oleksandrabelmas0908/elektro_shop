from rest_framework import serializers
from .models import Product, MyUser, OrderProducts, Orders

from django.contrib.auth import authenticate


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
    name = serializers.CharField(source='product_id.product_name')
    product_description = serializers.CharField(source='product_id.description')
    product_price = serializers.DecimalField(source='product_id.price_usd', max_digits=10, decimal_places=2)


    class Meta:
        model = OrderProducts
        fields = (
            "order_id",
            "name",
            "product_description",
            "product_price",
            "amount",
        )


class OrderGetSerializer(serializers.ModelSerializer):
    items = OrderProductsSerializer(source='orderproducts_set', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        total = sum(item.subtotal for item in obj.orderproducts_set.all())
        return total

    class Meta:
        model = Orders
        fields = (
            "order_id",
            "user_id",
            "created_at",
            "status",
            "total_price",
            "items",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = MyUser
        fields = ["email", "password", "first_name", "last_name", "is_staff", "is_superuser"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return MyUser.objects.create_user(password=password, **validated_data)
    

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password", code='authorization')

        attrs['user'] = user
        return attrs