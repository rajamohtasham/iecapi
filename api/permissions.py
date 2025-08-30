from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    SAFE_METHODS (GET, HEAD, OPTIONS) → allow anyone
    Write methods (POST, PUT, DELETE) → require authentication
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAuthenticatedForWrite(permissions.BasePermission):
    """
    Anyone can view, but only authenticated users can modify.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
