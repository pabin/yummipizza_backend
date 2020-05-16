from rest_framework import serializers

from .models import *



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'user_image', 'address', 'contact', 'first_name', 'last_name', 'last_login']
        depth = 1
