from rest_framework.permissions import BasePermission

class IsDefendantOrPlaintiff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.profile.role in ['DEFENDANT', 'PLAINTIFF']
        )

class IsJuror(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.profile.role == 'JUROR'
        )

class IsJudge(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.profile.role == 'JUDGE'
        )
