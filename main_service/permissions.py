from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Anonimowi i zalogowani użytkownicy mogą tylko odczytywać.
    Administrator — ma pełne uprawnienia.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAdminOrAuthenticatedCreateOnly(permissions.BasePermission):
    """
    - Anonimowi użytkownicy: tylko odczyt
    - Zalogowani użytkownicy: odczyt + tworzenie
    - Administrator: pełne uprawnienia
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        # Zalogowany użytkownik może tylko tworzyć
        return request.user and request.user.is_authenticated and request.method == "POST"
