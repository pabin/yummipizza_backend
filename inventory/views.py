from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.db import transaction
from django.shortcuts import get_object_or_404
import ast

from accounts.serializers import *
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

        serializer = ShoppingCartSerializer(data=request.data, partial=True)
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

    def put(self, request, pk, format=None):
        cart = get_object_or_404(ShoppingCart, id=pk)
        items = ast.literal_eval(request.data['items'])

        for item in items:
            cart.items.add(item)

        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)



""" Create Order Items and Order Instances, add order to User Instance """
class OrderCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user

        orderitem_serializer = OrderItemSerializer(data=request.data['order_items'], many=True)
        address_serializer = AddressSerializer(data=request.data['delivery_address'])
        contactdetail_serializer = ContactDetailSerializer(data=request.data['contact_detail'])

        if orderitem_serializer.is_valid() and address_serializer.is_valid() and contactdetail_serializer.is_valid():
            try:
                with transaction.atomic():
                    orderitem_serializer.save()
                    address_serializer.save()
                    contactdetail_serializer.save()

                    order = {
                        "total_price": request.data['total_price'],
                        "status": request.data['status'],
                        "delivery_address_id": address_serializer.data['id'],
                        "contact_detail_id": contactdetail_serializer.data['id'],
                    }

                    order_serializer = OrderSerializer(data=order, partial=True)
                    if order_serializer.is_valid():
                        order_serializer.save()

                        order_id = order_serializer.data['id']
                        user.orders.add(order_id)
                        order_obj = get_object_or_404(Order, id=order_id)

                        for order_item in orderitem_serializer.data:
                            order_obj.order_items.add(order_item['id'])

                        serializer = OrderSerializer(order_obj)
                        return Response(serializer.data)
                    else:
                        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True, "message": "Exception"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(orderitem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" List all User Orders """
class OrderListAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        user_orders = user.orders.all()
        print("user_orders", user_orders)
        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data)
