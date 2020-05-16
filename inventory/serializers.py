from rest_framework import serializers

from .models import *
from accounts.models import (
    Address,
    ContactDetail
)


class ItemInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemInventory
        exclude = ('item_reviews', 'ratings', 'created_at', 'is_active', )


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemInventorySerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemInventory.objects.all(), source='item', write_only=True
        )

    class Meta:
        model = OrderItem
        fields = '__all__'
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    delivery_address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source='delivery_address', write_only=True
        )
    contact_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=ContactDetail.objects.all(), source='contact_detail', write_only=True
        )

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1



class ShoppingCartSerializer(serializers.ModelSerializer):
    items_list = serializers.SerializerMethodField()
    # items = ItemInventorySerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        # depth = 1

    def get_items_list(self, obj):
        return ItemInventorySerializer(obj.items.all(), many=True).data
