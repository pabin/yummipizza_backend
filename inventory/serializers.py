from rest_framework import serializers
from django.db.models import Sum

from .models import *
from accounts.models import (
    Address,
    ContactDetail
)



class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ItemInventorySerializer(serializers.ModelSerializer):
    ratings_value = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    discount = DiscountSerializer()

    class Meta:
        model = ItemInventory
        exclude = ('item_reviews', 'ratings', 'views', 'created_at', 'is_active', )

    def get_ratings_value(self, obj):
        item_ratings = obj.ratings.all()

        ratings_count = item_ratings.count()
        rating_sum = item_ratings.aggregate(Sum('rating'))['rating__sum'] or 0
        average_rating = (rating_sum / ratings_count) if rating_sum > 0 else 0

        return ({"total_ratings": ratings_count, "average_rating": average_rating})

    def get_reviews_count(self, obj):
        return obj.item_reviews.all().count()



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


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    item = ItemInventorySerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemInventory.objects.all(), source='item', write_only=True
        )

    class Meta:
        model = ShoppingCartItem
        fields = '__all__'
        depth = 1


class ShoppingCartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def get_cart_items(self, obj):
        return ShoppingCartItemSerializer(obj.cart_items.all(), many=True).data
