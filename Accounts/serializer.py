from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username', 'password', 'email',]
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.password = make_password(validated_data.get('password'))
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance