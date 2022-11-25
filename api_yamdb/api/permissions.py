from rest_framework import permissions


class OwnerOrAdmins(permissions.BasePermission):
    """Разрешения для владельца и админов."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin)


class AuthorOrModeratorOrAdmin(permissions.BasePermission):
    """Разрешения для владельца, модераторов и админов."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class ReadOnly(permissions.BasePermission):
    """Разрешения для всех, только чтение."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Разрешения для админов."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
