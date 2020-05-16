from django.urls import path, include
from .views import *


urlpatterns = [
    path('items/', ItemInventoryListAPIView.as_view(), name='item_inventory_list'),
]
