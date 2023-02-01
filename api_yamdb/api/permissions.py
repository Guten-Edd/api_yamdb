from rest_framework import permissions
ADMIN_MESSAGE = 'Права администратора необходим'


class IsAdminOrModeratirOrAuthorOrReadOnly(permissions.BasePermission):
    """"Проверка прав для отзывов."""
    message = ADMIN_MESSAGE

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or request.user == obj.author
        )
