from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Override the method of BasePermission
    def has_object_permission(self, request, view, obj):
        # if the method is one of SAFE METHODS such as GET (READ)
        if request.method in permissions.SAFE_METHODS:
            # Permission granted
            return True
        # else if the user requesting is the owner of the object,
        # also grant access, otherwise do not!
        return obj.owner == request.user
