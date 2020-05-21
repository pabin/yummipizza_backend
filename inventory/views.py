from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
import ast

from accounts.serializers import *
from .serializers import *
from reviews.models import ItemRating



class CustomPagination(pagination.PageNumberPagination):
       page_size = 16


""" List all Item Inventory """
class ItemInventoryListAPIView(generics.ListAPIView):
    pagination_class=CustomPagination
    queryset = ItemInventory.objects.filter(is_active=True)
    serializer_class = ItemInventorySerializer



""" List Items based on user filter parameters """
class ItemFilterAPIView(generics.ListAPIView):
    serializer_class = ItemInventorySerializer
    pagination_class=CustomPagination

    def get_queryset(self):
        types = self.request.query_params.getlist('types[]')
        prices = self.request.query_params.getlist('prices[]')
        reviews = self.request.query_params.getlist('reviews[]')
        sort_by = self.request.query_params.get('sort_by')

        active = Q(is_active=True)
        itm_typ = Q(item_type__in=types) if types else Q()

        p1 = p2 = p3 = p4 = p5 = Q()

        for p in prices:
            print("p", p)
            if (p=="PRICE1"):
                p1 = Q(ls_price__gte=1, ls_price__lte=10)

            elif (p=="PRICE2"):
                p2 = Q(ls_price__gte=11, ls_price__lte=20)

            elif (p=="PRICE3"):
                p3 = Q(ls_price__gte=21, ls_price__lte=30)

            elif (p=="PRICE4"):
                p4 = Q(ls_price__gte=31, ls_price__lte=40)

            elif (p=="PRICE5"):
                p5 = Q(ls_price__gte=41)

        rev = rat = Q()
        for r in reviews:
            if (r=="REVIEWS"):
                rev =  Q(item_reviews__isnull=False)
            elif (r=="RATINGS"):
                rat =  Q(ratings__isnull=False)

        items = ItemInventory.objects.filter(active, itm_typ, p1 | p2 | p3 | p4 | p5, rev | rat)

        if (sort_by == "LOW_TO_HIGH"):
            return items.order_by('ls_price')
        elif (sort_by == "HIGHT_TO_LOW"):
            return items.order_by('-ls_price')
        elif (sort_by == "POPULARITY"):
            return items.order_by('-views')
        else:
            return items



""" List 6 most popular items """
class PopularItemListAPIView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    serializer_class = ItemInventorySerializer

    def get_queryset(self):
        popular_items = ItemInventory.objects.filter().order_by('-views')[:4]
        return popular_items



""" Update the Views of a Item """
class ItemRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    queryset = ItemInventory.objects.filter(is_active=True)
    serializer_class = ItemInventorySerializer

    def put(self, request, pk, format=None):
        item = get_object_or_404(ItemInventory, id=pk)
        item.views += 1
        item.save()
        return Response({"success": True})



""" Create Shopping Cart Instance, add to User Instance """
class ShoppingCartCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user


        cart_item = {
        "item_id": 1,
        "quantity": 1,
        "size": "MEDIUM"
        }

        cartitem_serializer = ShoppingCartItemSerializer(data=request.data['cart_item'])
        cart_serializer = ShoppingCartSerializer(data={"active":True}, partial=True)

        if cart_serializer.is_valid() and cartitem_serializer.is_valid():
            try:
                with transaction.atomic():
                    cartitem_serializer.save()
                    cart_serializer.save()

                    cart = get_object_or_404(ShoppingCart, id=cart_serializer.data['id'])
                    cart.cart_items.add(cartitem_serializer.data['id'])

                    user.carts.add(cart_serializer.data['id'])

                    serializer = ShoppingCartSerializer(cart)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" Retrieves or Updates Shopping Cart Instance """
class ShoppingCartRUAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def put(self, request, pk, format=None):
        cart = get_object_or_404(ShoppingCart, id=pk)

        # below line is required while testing from postman, but not from react app
        # items = ast.literal_eval(request.data['items'])

        serializer = ShoppingCartItemSerializer(data=request.data['cart_item'])

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    cart.cart_items.add(serializer.data['id'])

                    cart_serializer = ShoppingCartSerializer(cart)
                    return Response(cart_serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True, "message": "Exception"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" Retrieves or Updates or deletes Shopping Cart Instance """
class CartItemRUAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = ShoppingCartItem.objects.all()
    serializer_class = ShoppingCartItemSerializer


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

                        # Make current cart inactive after order is created
                        time_now = timezone.now()
                        valid_cart = user.carts.filter(validity__gte=time_now, is_active=True)[0]
                        valid_cart.is_active = False
                        valid_cart.save()

                        serializer = UserSerializer(user)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True, "message": "Exception"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(orderitem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" List all User Orders """
class OrderListAPIView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer


    """ Returns all the orders of authenticated user """
    def get_queryset(self):
        user = self.request.user
        return user.orders.all().order_by('-id')



""" List User Orders based on user order filter parameters """
class OrderFilterAPIView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        dates = self.request.query_params.getlist('dates[]')
        prices = self.request.query_params.getlist('prices[]')
        status = self.request.query_params.getlist('status[]')

        print('----------------')
        print("dates", dates)
        print("prices", prices)
        print("status", status)

        active = Q(is_active=True)
        status = Q(status__in=status) if status else Q()

        p1 = p2 = p3 = p4 = p5 = Q()

        for p in prices:
            print("p", p)
            if (p=="PRICE1"):
                p1 = Q(total_price__gte=1, total_price__lte=50)

            elif (p=="PRICE2"):
                p2 = Q(total_price__gte=51, total_price__lte=100)

            elif (p=="PRICE3"):
                p3 = Q(total_price__gte=101, total_price__lte=200)

            elif (p=="PRICE4"):
                p4 = Q(total_price__gte=201)

        last_7 = timezone.now().date() - timedelta(days=7)
        last_14 = timezone.now().date() - timedelta(days=14)

        ths_week = lst_week = all = Q()
        for d in dates:
            if (d=="THIS_WEEK"):
                ths_week =  Q(ordered_at__gte=last_7)
            elif (d=="LAST_WEEK"):
                lst_week =  Q(ordered_at__gte=last_14, ordered_at__lte=last_7)

        orders = user.orders.filter(active, status, p1 | p2 | p3 | p4, ths_week | lst_week)
        return orders.order_by('-id')
