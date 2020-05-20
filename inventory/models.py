from django.db import models
from django.core.validators import URLValidator
from datetime import timedelta
from django.utils import timezone
import pytz



""" Item Inventory, mostly Pizzas, defines attributes of Pizza"""
class ItemInventory(models.Model):
    TYPE_CHOICES = [
        ("VEG", "Veg"),
        ("NON_VEG", "Non Veg")
    ]

    name = models.CharField(max_length=64)
    ms_price = models.IntegerField()
    ls_price = models.IntegerField()

    item_type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    item_image = models.TextField(validators=[URLValidator()])

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    # Item Reviews and ratings
    item_reviews = models.ManyToManyField('reviews.ItemReview')
    ratings = models.ManyToManyField('reviews.ItemRating')

    # For finding popular pizzas
    views = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.name} - Medium: {self.ms_price} Large: {self.ls_price} "

    def avg_rating(self):
        item_ratings = self.ratings.all()

        ratings_count = item_ratings.count()
        rating_sum = item_ratings.aggregate(models.Sum('rating'))['rating__sum'] or 0
        average_rating = rating_sum / ratings_count if rating_sum > 0 else 0

        return average_rating



""" OrderItem Table, Contains Item from ItemInventory model """
class OrderItem(models.Model):
    SIZE_CHOICES = [
        ("LARGE", "Large"),
        ("MEDIUM", "Medium")
    ]

    item = models.ForeignKey('inventory.ItemInventory', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.item} - {self.quantity}"



""" Order Table, defines attributes of order, can have multiple order items"""
class Order(models.Model):
    ORDER_STATUS = [
        ("PENDING", "Pending"),
        ("DELIVERED", "Delivered"),
        ("ON_HOLD", "On Hold"),
        ("CANCELLED", "Cancelled")
    ]

    order_items = models.ManyToManyField('inventory.OrderItem')
    total_price = models.IntegerField()

    delivery_address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, null=True)
    contact_detail = models.ForeignKey('accounts.ContactDetail', on_delete=models.SET_NULL, null=True)

    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=ORDER_STATUS)

    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"Total Items: {self.order_items.all().count()} - Total Price: {self.total_price}"




""" Shopping Cart Item Table, Contains items selected by user """
class ShoppingCartItem(models.Model):
    SIZE_CHOICES = [
        ("LARGE", "Large"),
        ("MEDIUM", "Medium")
    ]

    item = models.ForeignKey('inventory.ItemInventory', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.item} - {self.quantity}"


""" Shopping Cart Table, defines atrributes of Shopping cart  """
class ShoppingCart(models.Model):
    cart_items = models.ManyToManyField('inventory.ShoppingCartItem')

    is_active = models.BooleanField(default=True)
    validity = models.DateTimeField()


    def save(self, *args, **kwargs):
        """ Add Validity on Shooping Cart save """
        if not self.pk:
            validity = timezone.now() + timedelta(0, 600) # Add 10 minutes validity
            self.validity = validity
        return super(ShoppingCart, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.validity}"
