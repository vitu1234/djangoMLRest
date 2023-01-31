from rest_framework import serializers
from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


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



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        token = self.get_token(self.user)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        data['error'] = False
        data['msg'] = "Logged in user"
        
        return data


