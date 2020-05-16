from django.urls import path, include
from .views import *


urlpatterns = [
    path('items/', ItemInventoryListAPIView.as_view(), name='item_inventory_list'),
    path('cart/', ShoppingCartCreateAPIView.as_view(), name='shopping_cart_create'),
    path('cart/<int:pk>/', ShoppingCartRUAPIView.as_view(), name='cart_retrieve_update'),
    path('order/', OrderCreateAPIView.as_view(), name='order_create'),
    path('user-orders/', OrderListAPIView.as_view(), name='user_orders'),
]
