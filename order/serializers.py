from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from order.models import Order, OrderItem
from authentication.models import User
from authentication.serializers import UserSerializer
from store.models import Product
from store.serializers import ProductSerializer

class OrderSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    placed_by = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_products(self, order):
        product_queryset = OrderItem.objects.filter(order=order).values_list('product', 'quantity', 'amount')
        products = []
        included_fields = ('category', 'id', 'image', 'name', 'price', 'is_available')
        for item in list(product_queryset):
            product_obj = ProductSerializer(Product.objects.get(id=item[0]), fields=included_fields).data
            products.append({'product': product_obj, 'quantity': item[1], 'amount': item[2]})
        return products

    def get_placed_by(self, order):
        user: User = User.objects.get(id=order.placed_by_id)
        included_fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'full_name')
        return UserSerializer(user, fields=included_fields).data


class OrderItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('deleted', 'created_on', 'updated_on')
