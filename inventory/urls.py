from django.urls import path, include
from .views import *


urlpatterns = [
    path('items/', ItemInventoryListAPIView.as_view(), name='item_inventory_list'),
    path('items-filter/', ItemFilterAPIView.as_view(), name='items_filter_list'),

    path('cart/', ShoppingCartCreateAPIView.as_view(), name='shopping_cart_create'),
    path('cart/<int:pk>/', ShoppingCartRUAPIView.as_view(), name='cart_retrieve_update'),
    path('cart-item/<int:pk>/', CartItemRUAPIView.as_view(), name='cart_item_retrieve_update'),

    path('order/', OrderCreateAPIView.as_view(), name='order_create'),
    path('user-orders/', OrderListAPIView.as_view(), name='user_orders'),
    path('order-filter/', OrderFilterAPIView.as_view(), name='order_filter'),

    path('popular-items/', PopularItemListAPIView.as_view(), name='popular_items_list'),
    path('item/<int:pk>/', ItemRetrieveUpdateAPIView.as_view(), name='update_item_views'),
]
