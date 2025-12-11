from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow owners of an object to edit/delete it; others read-only."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the object's author
        return getattr(obj, 'author', None) == request.user