from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Позволяет только просмотр для всех.
    Изменение — только для админа.
    """
    def has_permission(self, request, view):
        # Чтение — для всех
        if request.method in SAFE_METHODS:
            return True
        # Запись — только админ
        return request.user and request.user.is_staff


class IsAuthenticatedForWriteOnly(BasePermission):
    """
    Только аутентифицированные могут создавать (POST).
    Все могут просматривать (GET).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

