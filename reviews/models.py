from django.db import models
from django.core.validators import (
    MinValueValidator
    MaxValueValidator,
)



""" Item Reviews Table """
class ItemReview(models.Model):
    message = models.TextField()
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_archived = models.BooleanField(default=False)  # On Review delete by User

    def __str__(self):
        return f"{self.user} - {self.message}"



""" Item Ratings Table, Rating Value will be from 1 to 5  """
class ItemRating(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.rating}"
