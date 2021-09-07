from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from order.models import Order, OrderItem

class OrderSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_products(self, order):
        product_queryset = list(OrderItem.objects.filter(order=order).values_list(
                                            'product__name', 'quantity', flat=True))
        products = list()
        for item in product_queryset:
            products.append({'product': item[0], 'quantity': item[1]})
        return products

class OrderItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        exclude = ('deleted', 'created_on', 'updated_on')

    def get_amount(self, instance):
        return instance.amount
