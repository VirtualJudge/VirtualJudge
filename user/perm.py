from rest_framework import permissions


class ManageUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.has_perms('user.manage_user')