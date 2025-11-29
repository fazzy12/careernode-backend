from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)

User = get_user_model()

# --- 1. Authentication Endpoints ---

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns JWT tokens + User Role/ID.
    """
    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordView(APIView):
    """
    POST /api/auth/password/change/
    Allows logged-in users to change their password.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"message": "Password updated successfully."}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- 2. User Management Endpoints ---

class UserProfileView(APIView):
    """
    GET/PATCH /api/auth/me/
    DELETE /api/users/me/
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request):
        serializer = UserSerializer(self.get_object())
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        self.get_object().delete()
        return Response({"message": "Account deleted."}, status=status.HTTP_204_NO_CONTENT)

# --- 3. Admin Endpoints -----

class AdminUserListView(generics.ListAPIView):
    """
    GET /api/users/
    List all users (Admin only).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class AdminUserDetailView(generics.DestroyAPIView):
    """
    DELETE /api/users/{id}/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)