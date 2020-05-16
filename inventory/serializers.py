from rest_framework import serializers

from .models import *



class ItemInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemInventory
        exclude = ('item_reviews', 'ratings', 'created_at', 'is_active', )


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        depth = 1
