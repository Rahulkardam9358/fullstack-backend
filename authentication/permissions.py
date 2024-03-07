from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and 
            request.user.is_superuser 
        )


class IsOwner(permissions.BasePermission):
    message = 'To perform this action you must be an owner'

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )


    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.user


class IsDeveloper(permissions.BasePermission):
    message = "You must have developer account to view this page."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Developer').exists()