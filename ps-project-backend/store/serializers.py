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
        cart_items_queryset = CartItem.objects.filter(cart=instance).values_list('product_id','product__image', 'product__name', 'product__price', 'quantity')
        cart_items = list()
        for item in list(cart_items_queryset):
            data = {'product_id': item[0], 'image': item[1], 'name': item[2], 'price': item[3], 'quantity': item[4]}
            data.update({'amount': data['price'] * data['quantity']})
            cart_items.append(data)
        return cart_items

    def to_representation(self, instance):
        data = super(CartSerializer, self).to_representation(instance)
        amt = 0.0
        for item in data['cart_items']:
            amt += item['amount']
        data['total_amount'] = amt
        return data

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