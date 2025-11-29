from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    CustomTokenObtainPairView, 
    UserProfileView, 
    AdminUserListView,
    AdminUserDetailView,
    ChangePasswordView
)

urlpatterns = [
    # --- Auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth_login'), # Using Custom View
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password/change/', ChangePasswordView.as_view(), name='auth_password_change'),

    # --- Profile
    path('auth/me/', UserProfileView.as_view(), name='auth_me'),
    path('users/me/', UserProfileView.as_view(), name='users_delete_me'),
    
    # --- Admin Users
    path('users/', AdminUserListView.as_view(), name='admin_user_list'), # New List View
    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
]