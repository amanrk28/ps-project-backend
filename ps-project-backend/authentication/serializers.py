from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'is_admin', 'is_store_owner', 'phone_number', 'email',
                  'address', 'full_name']

    def get_full_name(self, instance):
        return instance.fullname