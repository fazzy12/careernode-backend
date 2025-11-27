from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserProfileView, AdminUserDetailView

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile (Me)
    path('auth/me/', UserProfileView.as_view(), name='profile'),
    path('users/me/', UserProfileView.as_view(), name='delete_profile'),

    # Admin
    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_delete'),
]