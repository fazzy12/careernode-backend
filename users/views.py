# careernode-backend/users/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

# --- 1. Authentication Endpoints ---

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Creates a new account. Returns 201 on success or 400 with validation errors.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# --- 2. User Management Endpoints ---

class UserProfileView(APIView):
    """
    Handles operations for the currently logged-in user.
    
    GET /api/auth/me/
    - Returns 200 OK with user profile data.
    
    PATCH /api/auth/me/
    - Returns 200 OK on success.
    - Returns 400 Bad Request with validation errors (e.g., {"email": ["Enter a valid email address."]}).
    
    DELETE /api/users/me/
    - Returns 204 No Content on successful deletion.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # request.user is guaranteed to exist because of IsAuthenticated
        return self.request.user

    def get(self, request):
        serializer = UserSerializer(self.get_object())
        return Response(serializer.data)

    def patch(self, request):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # Professional handling: Return specific validation errors with 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object()
        user.delete()
        return Response(
            {"message": "Account deleted successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )

class AdminUserDetailView(generics.DestroyAPIView):
    """
    DELETE /api/users/{id}/
    Admin only endpoint to ban/remove a specific user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)