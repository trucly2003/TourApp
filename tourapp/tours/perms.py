from rest_framework import permissions
from rest_framework.permissions import BasePermission

class OwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.user

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):    
        return request.user.is_superuser

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'customer')

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'staff')