from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.hashers import make_password

from .serializers import *



""" User Authentication API, Returns Token and User details """
class UserAuthenticationAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        return Response({
            'token': token.key,
            'user': UserSerializer(token.user).data
            }, status=status.HTTP_200_OK)



""" Retrieves and Updates User Instance """
class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


    """ Update user profile data like name, username """
    def put(self, request, pk, format=None):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" Create new User account """
class UserCreateAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):

        try:
            user = User.objects.get(username=request.data['username'])
            return Response({"message", "Username already exist!"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            # User does not exist, create new
            hashed_password = make_password(request.data['password'])
            data = {
                "username": request.data['username'],
                "password": hashed_password,
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "user_image": request.data['user_image'],
            }
            serializer = UserSerializer(data=data, partial=True)
            try:
                with transaction.atomic():
                    if serializer.is_valid():
                        serializer.save()
                        user = User.objects.get(id=serializer.data['id'])
                        token = Token.objects.create(user=user)

                        return Response({
                            'token': token.key,
                            'user': UserSerializer(token.user).data
                            }, status=status.HTTP_200_OK)

            except Exception as e:
                print("Exception: ", e)
                return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
