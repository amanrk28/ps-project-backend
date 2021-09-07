from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from .models import Product, Cart, CartItem

class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        exclude = ('deleted', 'created_on', 'updated_on')

    def get_cart_items(self, instance):
        return list(CartItem.objects.filter(cart=instance).values_list('product_id', flat=True))


class CartItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    cart_count = serializers.SerializerMethodField(read_only=True)
    cart = CartSerializer(fields=('hash',), read_only=True)
    amount = serializers.SerializerMethodField(read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(write_only=True, source='cart', queryset=Cart.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, source='product', queryset=Product.objects.all())
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        exclude = ('deleted', 'created_on', 'updated_on', 'id')

    def get_product(self, instance):
        excluded_fields = ('deleted', 'created_on', 'updated_on')
        return ProductSerializer(instance.product, context=self.context, exclude=excluded_fields).data

    def get_cart_count(self, instance):
        return CartItem.objects.filter(cart=instance.cart).count()

    def get_amount(self, instance):
        return instance.product.price * instance.quantity