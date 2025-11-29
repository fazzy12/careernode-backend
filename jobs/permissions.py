from rest_framework import permissions

class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow any user to list jobs,
    but only Employers can create them.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'employer'
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a job (or Admin) to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.employer == request.user or request.user.is_superuser