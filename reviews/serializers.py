from rest_framework import serializers

from .models import *
from accounts.models import User
from accounts.serializers import BasicUserProfileSerializer



class ItemReviewSerializer(serializers.ModelSerializer):
    user = BasicUserProfileSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
        )

    class Meta:
        model = ItemReview
        exclude = ('updated_at', 'is_archived', )


class ItemRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRating
        exclude = ('updated_at', )
