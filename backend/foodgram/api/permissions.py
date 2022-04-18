from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorIsStaffOrReadOnly(BasePermission):
    """Удаление/добавление/изменение доступно автору и персоналу.
    Остальным доступно только чтение.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or
                    obj.author == request.user or
                    request.user.is_staff)


class MeOnlyForAuthenticated(BasePermission):
    """Текущий пользователь доступен только авторизованному пользователю.
    Просмотр списка пользователей и профиля пользователя доступно всем.
    """

    def has_permission(self, request, view):
        return bool(not (view.action == 'me' and request.user.is_anonymous))
