from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ["id", "username", "first_name", "last_name", "email", "password"]

  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['email'],
      username=validated_data['username'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
    )
    user.set_password(validated_data['password'])
    
    
    user.save()
    return user
   


