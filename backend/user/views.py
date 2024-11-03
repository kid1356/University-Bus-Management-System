from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status,permissions
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
    


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        serializer = ChangePasswordSerializer(data = request.data, context = {'user':request.user})
        serializer.is_valid(raise_exception=True)

        return Response({'message':"Password change successfully"},status=status.HTTP_200_OK)



class ForgetPassowrdEmailSendView(APIView):
    def post(self, request):
        serializer = ForgetPassowrdEmailSendSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({"message":"An Email is sent"},status=status.HTTP_200_OK)
    

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTP(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message":"OTP Confirmed"},status=status.HTTP_200_OK)
    


class ForgetPasswordChangeView(APIView):
    def post(self, request):
        serializer = ForgetPasswordResetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message":"password reset successfully "},status=status.HTTP_200_OK)