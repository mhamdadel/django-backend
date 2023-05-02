from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True},
        }

    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('First name must be at least 2 characters long.')
        return value

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Last name must be at least 2 characters long.')
        return value

    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Phone number must be at least 10 digits long.')
        if len(value) > 15:
            raise serializers.ValidationError('Phone number must be at most 15 digits long.')
        return value

    def validate(self, data):
        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email address is already in use.')
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect credentials')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        data['id'] = instance.id
        data['first_name'] = instance.first_name
        data['last_name'] = instance.last_name
        data['is_authenticated'] = instance.is_authenticated
        return data