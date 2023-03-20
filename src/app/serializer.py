from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from .models import *

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=45)
    email = serializers.CharField(max_length=80)
    phone = serializers.CharField(max_length=45)
    type_acteur = serializers.CharField(max_length=250)
    acteur = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=45, write_only=True)
    
    class Meta:
        model = User
        fields = ['id' ,'username', 'email','phone', 'type_acteur', 'acteur', 'description', 'password']
        
    
    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs['username']).exists()
        email_exists = User.objects.filter(email=attrs['email']).exists()
        phone_exists = User.objects.filter(phone=attrs['phone']).exists()
        """
        if username_exists:
            raise ValidationError("username exists déjà")
        
        if email_exists:
            raise ValidationError("email exists déjà")
        
        if phone_exists:
            raise ValidationError("numero de téléphone exists déjà")
        
        """
        return super().validate(attrs)
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

class TypeActeurSerialiser(serializers.ModelSerializer):
    class Meta:
        model = TypeActeur
        fields = ['id', 'code_type_acteur', 'nom_type_acteur', 'libele']