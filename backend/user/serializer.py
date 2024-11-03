from rest_framework import serializers
from .models import *
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.utils import timezone


class Email_send:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(subject= data['subject'],
                             body=data['body'],
                             to=[data['to_email']])
        email.send()


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style = {'input_type':'password'},write_only = True)
    
    class Meta:
        model = User
        fields = ['email','username','full_name','role','university','picture','password','confirm_password']
        extra_kwargs = {
            'email':{'required':True},
            'username':{'required':True},
            'role':{'required':True},
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')


        if password != confirm_password:
            raise serializers.ValidationError("Both password should be match")
        

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 254)

    class Meta:
        model = User
        fields = ['email','password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password= serializers.CharField(max_length = 100, style = {'input_type':'password'},write_only = True)
    confirm_password= serializers.CharField(max_length = 100, style = {'input_type':'password'},write_only = True)

    class Meta:
        model = User
        fields = ['password','confirm_password']

    def validate(self, attrs):
        password=attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')

        if password !=  confirm_password:
            raise serializers.ValidationError("Both password should be same")
    
        user.set_password(password)
        user.save
        return attrs
        

class ForgetPassowrdEmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)


    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("no user found with this email")
        

        otp_value  = get_random_string(length=4 , allowed_chars='0123456789')

        data = {
            'subject':'Your password reset otp',
            'body':f'Your OTP is {otp_value}',
            'to_email':user.email
        }

        user.otp = otp_value
        user.otp_created_at = timezone.now()
        user.save()

        Email_send.send_mail(data)

        return attrs
    
class VerifyOTP(serializers.ModelSerializer):
    otp_value = serializers.CharField(max_length = 5)
    email = serializers.EmailField(max_length = 100)
    class Meta:
        model = User
        fields = ['otp_value','email']

    def validate(self, attrs):
        otp_value = attrs.get('otp_value')
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("User not Found") 

        if user.otp != otp_value:
            raise serializers.ValidationError("Incorrect OTP")
        
        if user.otp_created_at + timezone.timedelta(minutes=5) < timezone.now():
            raise serializers.ValidationError("OTP Expired")
        

        return attrs
        
        





class ForgetPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    password= serializers.CharField(max_length = 100, style = {'input_type':'password'},write_only = True)
    confirm_password= serializers.CharField(max_length = 100, style = {'input_type':'password'},write_only = True)
    

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("User not Found")
        
        if password != confirm_password:
            raise serializers.ValidationError("Both passowrd should be same")
        
        attrs['user']  = user
    

        return attrs
    
    def create(self, validated_data):
        user = validated_data['user']
        user.set_password(validated_data['password'])
  
        user.otp = ''
        user.otp_created_at  =None
        user.save()


        return user


     