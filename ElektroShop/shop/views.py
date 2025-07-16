from django.core.serializers import serialize
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Orders
from rest_framework.response import Response
from rest_framework import status


def say_hello(request):
    return JsonResponse({"data": "Hello nigga"})


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


class UserInfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  
            'auth': str(request.auth),  
        }
        return Response(content)
    
    def post(self, request, format=None):
        data = request.data
        if 'name' in data and 'email' in data:
            return Response({"message": "User info received", "name": data['name'], "email": data['email']}, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)