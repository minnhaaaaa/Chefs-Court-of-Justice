from rest_framework.permissions import BasePermission

class IsPlaintiffOrDefendant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.profile.role in ['PLAINTIFF', 'DEFENDANT']
        )
