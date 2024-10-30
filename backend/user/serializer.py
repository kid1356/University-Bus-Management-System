from rest_framework import serializers
from .models import *


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