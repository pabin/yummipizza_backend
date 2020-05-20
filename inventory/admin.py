from django.contrib import admin

from .models import *

admin.site.register(ItemInventory)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
