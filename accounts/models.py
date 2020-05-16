from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator



""" User Table, defines attributes of a User """
class User(AbstractUser):
    class Meta:
        default_permissions = ()

    address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey('accounts.ContactDetail', on_delete=models.SET_NULL, null=True)
    user_image = models.TextField(validators=[URLValidator()])

    orders = models.ManyToManyField('inventory.Order')
    carts = models.ManyToManyField('inventory.ShoppingCart')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


""" Address Table, defines atrributes of Address """
class Address(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

    state = models.CharField(max_length=32)
    zip_code = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.city} : {self.state}"


""" Contact Details Table, defines attributes of Contact Details """
class ContactDetail(models.Model):
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=32)

    def __str__(self):
        return f"{self.mobile} - {self.email}"
