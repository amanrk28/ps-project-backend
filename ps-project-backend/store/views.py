from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException, PermissionDenied

from .models import ProductItem, Cart, CartItem
from .serializers import ProductItemSerializer, CartItemSerializer, CartSerializer
# Create your views here.
class ProductItemList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer

class ProductItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer

class CartItemList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

