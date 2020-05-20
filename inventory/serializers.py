from rest_framework import serializers
from django.db.models import Sum

from .models import *
from accounts.models import (
    Address,
    ContactDetail
)


class ItemInventorySerializer(serializers.ModelSerializer):
    ratings_value = serializers.SerializerMethodField()

    class Meta:
        model = ItemInventory
        exclude = ('item_reviews', 'ratings', 'created_at', 'is_active', )

    def get_ratings_value(self, obj):
        item_ratings = obj.ratings.all()

        ratings_count = item_ratings.count()
        rating_sum = item_ratings.aggregate(Sum('rating'))['rating__sum'] or 0
        average_rating = (rating_sum / ratings_count) if rating_sum > 0 else 0 

        return ({"total_ratings": ratings_count, "average_rating": average_rating})


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
