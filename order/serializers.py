from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from order.models import Order, OrderItem
from authentication.models import User
from authentication.serializers import UserSerializer

class OrderSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    placed_by = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_products(self, order):
        product_queryset = OrderItem.objects.filter(order=order).values_list('product', 'quantity', 'product__price')
        products = []
        for item in list(product_queryset):
            products.append({'product': item[0], 'quantity': item[1], 'amount': item[2] * item[1]})
        return products

    def get_placed_by(self, order):
        user: User = User.objects.get(id=order.placed_by_id)
        return UserSerializer(user).data


class OrderItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        exclude = ('deleted', 'created_on', 'updated_on')

    def get_amount(self, instance):
        return instance.amount
