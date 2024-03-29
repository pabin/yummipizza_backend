from django.urls import path, include
from .views import *


urlpatterns = [
    path('items-reviews/', ItemReviewListAPIView.as_view(), name='item_reviews_list'),
    path('review/<int:item_id>/', ItemReviewCreateAPIView.as_view(), name='item_review_create'),
    path('item-ratings/', ItemRatingView.as_view(), name='item_rating'),
    path('rating/<int:item_id>/', ItemRatingCreateAPIView.as_view(), name='item_rating_create'),
]
