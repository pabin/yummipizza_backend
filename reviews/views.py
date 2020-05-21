from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from .serializers import *
from inventory.models import ItemInventory
from inventory.serializers import ItemInventorySerializer



""" List all Item Reviews of a Item, with pagination """
class ItemReviewListAPIView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    queryset = ItemReview.objects.filter(is_archived=False)
    serializer_class = ItemReviewSerializer

    def get_queryset(self):
        item_id = self.request.query_params.get('item_id')
        item =  get_object_or_404(ItemInventory, id=item_id)
        return item.item_reviews.all()



""" Create Item Reviews, and add to Item Inventory Instance """
class ItemReviewCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, item_id, format=None):
        item =  get_object_or_404(ItemInventory, id=item_id)

        serializer = ItemReviewSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    item.item_reviews.add(serializer.data['id'])
                    return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" Get Total Ratings count and Average Item Ratings of a Item """
class ItemRatingView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        item_id = request.query_params.get('item_id')
        item =  get_object_or_404(ItemInventory, id=item_id)
        item_ratings = item.ratings.all()

        ratings_count = item_ratings.count()
        rating_sum = item_ratings.aggregate(Sum('rating'))['rating__sum']
        average_rating = rating_sum / ratings_count

        return Response({"total_ratings": ratings_count, "average_rating": average_rating}, status=status.HTTP_200_OK)



""" Create Item Rating, and add to Item Inventory Instance """
class ItemRatingCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, item_id, format=None):
        item =  get_object_or_404(ItemInventory, id=item_id)

        try:
            user_rating = item.ratings.filter(user=request.user)[0]
            serializer = ItemRatingSerializer(user_rating, data=request.data)
            if serializer.is_valid():
                serializer.save()

                item_serializer = ItemInventorySerializer(item)
                return Response(item_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            """ No User rating for this item, create new rating  """
            serializer = ItemRatingSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        serializer.save()
                        item.ratings.add(serializer.data['id'])

                        item_serializer = ItemInventorySerializer(item)
                        return Response(item_serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    print("Exception: ", e)
                    return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
