from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404

from accounts.serializers import UserSerializer
from .serializers import *


""" List all Item Inventory """
class ItemInventoryListAPIView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = ItemInventory.objects.filter(is_active=True)
    serializer_class = ItemInventorySerializer



""" Create Shopping Cart Instance, add to User Instance """
class ShoppingCartCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user
        print(user)
        print(typeof(user))

        # user_serializer = UserSerializer(user)
        # orderitem_serializer = OrderItemSerializer(data=request.data)

        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    user.carts.add(serializer.data['id'])
                    return Response(serializer.data)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True, "message": "Exception"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" Retrieves or Updates Shopping Cart Instance """
class ShoppingCartRUAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer



""" Create Oorder Items and Order Instances, add order to User Instance """
class OrderCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user
        print(user)
        print(typeof(user))

        # user_serializer = UserSerializer(user)
        # orderitem_serializer = OrderItemSerializer(data=request.data)

        orderitem_serializer = OrderItemSerializer(data=request.data, many=True)
        order_serializer = OrderSerializer(data=request.data)
        if orderitem_serializer.is_valid() and order_serializer.is_valid():
            try:
                with transaction.atomic():
                    orderitem_serializer.save()
                    order_serializer.save()
                    user.orders.add(order_serializer.data['id'])
                    return Response(order_serializer.data)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True, "message": "Exception"})
        return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)
