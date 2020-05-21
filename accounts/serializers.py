from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone

from inventory.serializers import ShoppingCartSerializer
from .models import *



class UserSerializer(serializers.ModelSerializer):
    valid_cart = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'valid_cart', 'username', 'password', 'user_image', 'address', 'contact', 'first_name', 'last_name', 'last_login']
        depth = 1

    def get_valid_cart(self, obj):
        time_now = timezone.now()
        valid_cart = obj.carts.filter(validity__gte=time_now, is_active=True).order_by('-id')

        if valid_cart:
            return ShoppingCartSerializer(valid_cart[0]).data
        return None


class BasicUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_image']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = "__all__"
