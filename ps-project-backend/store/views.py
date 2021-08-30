from django.shortcuts import render
from rest_framework import generics

from .models import ProductItem, Cart, CartItem
from .serializers import ProductItemSerializer, CartItemSerializer, CartSerializer
# Create your views here.
class ProductItemList(generics.ListCreateAPIView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer

class ProductItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer

class CartItemList(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


