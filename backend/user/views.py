from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

def generate_token(user):
    token = RefreshToken.for_user(user)

    return {
        'refresh':str(token),
        'access': str(token.access_token)
    }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token  = generate_token(user)
        return Response({"token":token,'register successfully':serializer.data}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data =request.data)
        serializer.is_valid(raise_exception=True)

        email  = serializer.data.get('email')
        password = serializer.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            token = generate_token(user)
            info = {
                    'id':user.id,
                    'username':user.username,
                    'role':user.role,
            }
            return Response({'token':token,'login successfully':info},status=status.HTTP_200_OK)
            
        return Response("login credential invalid",status=status.HTTP_400_BAD_REQUEST)