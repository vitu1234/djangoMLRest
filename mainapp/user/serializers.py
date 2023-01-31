from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import (
    User
)

#Serializer to Get User Details using Django Token Authentication


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["_id", "first_name","last_name","email"]

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

 
#---------------------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """'''
    email = serializers.EmailField(
        required=True
    )'''
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 
         'email', 'first_name', 'last_name')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     # instance.email = validated_data.get('email', instance.email)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.user_type = validated_data.get(
    #         'user_type', instance.user_type)
    #     # instance.users_id = validated_data.get('users_id', instance.users_id)
    #     instance.secret_key = validated_data.get(
    #         'secret_key', instance.secret_key)
    #     instance.private_key = validated_data.get(
    #         'private_key', instance.private_key)
    #     instance.public_key = validated_data.get(
    #         'public_key', instance.public_key)
    #     instance.save()

    #     return instance
  