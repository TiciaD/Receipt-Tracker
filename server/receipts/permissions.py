from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Receipt, Tag

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        elif isinstance(obj, Receipt):
            return obj.user == request.user
        return False

# class IsOwnerOrReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.user == request.user


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        print(request)
        return obj == request.user
