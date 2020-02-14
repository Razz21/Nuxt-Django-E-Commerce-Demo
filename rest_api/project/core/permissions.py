from rest_framework import permissions


class AccessOwnData(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class IsADmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
