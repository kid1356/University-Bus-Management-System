from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register-user'),
    path('login/',LoginView.as_view(),name='login-user'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('send-mail/',ForgetPassowrdEmailSendView.as_view(),name='forget-password-mail'),
    path('verify-otp/',VerifyOTPView.as_view(),name='otp-verify'),
    path('forget-password/',ForgetPasswordChangeView.as_view(),name='forget-password-reset'),


]