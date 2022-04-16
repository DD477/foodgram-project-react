from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user.is_staff)


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or
                    obj.author == request.user)


class IsAuthenticatedOrMeOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(not (view.action == 'me' and request.user.is_anonymous))
