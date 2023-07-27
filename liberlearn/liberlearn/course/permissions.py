from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to non-admin users and
    full access to admin users.
    """

    def has_permission(self, request, view):
        # Allow all users to have read-only access (GET, HEAD, OPTIONS)
        # to the view.
        if request.method in SAFE_METHODS:
            return True

        # Allow admin users to have full access (POST, PUT, DELETE)
        # to the view.
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
