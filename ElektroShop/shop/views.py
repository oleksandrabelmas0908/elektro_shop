from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Orders
from rest_framework.response import Response
from rest_framework import status


def say_hello(request):
    return HttpResponse("Hello nigga")


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


