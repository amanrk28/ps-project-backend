from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from .models import Product, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    cart_count = serializers.SerializerMethodField(read_only=True)
    cart = CartSerializer(fields=('hash',), read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(write_only=True, source='cart', queryset=Cart.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, source='product', queryset=Product.objects.all())
    product = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

    def get_product(self, instance):
        return ProductSerializer(instance.product, context=self.context).data

    def get_cart_count(self, instance):
        return CartItem.objects.filter(cart=instance.cart).count()