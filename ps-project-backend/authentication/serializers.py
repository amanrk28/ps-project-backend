from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'full_name', 'email', 'phone_number',
                  'is_store_owner', 'is_admin', 'username', 'address')

    def get_full_name(self, instance):
        return instance.fullname