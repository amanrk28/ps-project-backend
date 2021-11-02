from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from .models import User
from store.models import Cart, CartStatus

class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_cart_empty = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'full_name', 'email', 'phone_number',
                  'is_store_owner', 'is_admin', 'username', 'address','is_cart_empty')

    def get_full_name(self, instance):
        return instance.fullname

    def get_is_cart_empty(self, instance):
        try:
            cart = Cart.objects.filter(user=instance, status=CartStatus.NEW)
            if len(cart) > 0:
                return False
            return True
        except Cart.DoesNotExist:
            return True
