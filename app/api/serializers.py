from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import AddCity2,Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password','id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerailzer(serializers.ModelSerializer):
    user = UserSerializer(required=True )
    class Meta:
        model = Profile
        fields = '__all__'

class CitiesSerializer(serializers.ModelSerializer):
    profile=ProfileSerailzer
    class Meta:
        model = AddCity2
        fields = ['city','description','temperatuer','alertAbove','alertBelow']