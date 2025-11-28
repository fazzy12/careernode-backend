from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# --- 1. Core User Serializers ---

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing user profiles.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'created_at')
        read_only_fields = ('id', 'role', 'created_at')

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'applicant')
        )
        return user

# --- 2. Custom Auth Serializers ---

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Serializer to include User Role & ID in the login response.
    """
    def validate(self, attrs):
        # Get the standard JWT tokens (access/refresh)
        data = super().validate(attrs)

        # Add data to the response
        data.update({
            'user_id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'role': self.user.role,  #  for frontend routing
        })
        return data

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)