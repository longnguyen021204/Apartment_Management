from rest_framework import permissions

class OwnerPerms(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return self.has_permission(request, view) and request.user == obj.user
