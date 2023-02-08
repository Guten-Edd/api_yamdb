from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
            and (request.user.role == 'admin'
            or request.user.is_superuser))         
        )


class AdminOrSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        ''' Вариант работы с PUT-запросом, который не проходит pytest.
            Код ошибки 403 вместо 405
        if request.method == 'PUT':
            return False'''
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class AuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or request.user.username == obj.author.username
        )


'''class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user 
            or request.method in SAFE_METHODS
        )'''
