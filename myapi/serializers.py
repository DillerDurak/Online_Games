from rest_framework import serializers
from main.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class AvatarSerializer(serializers.Serializer):
    image = serializers.CharField(max_length=150)
