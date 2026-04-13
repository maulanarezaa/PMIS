from .models import UserRole, RolePermission

def user_has_permission(user, kode_permission):
    roles = UserRole.objects.filter(user=user).values_list('role', flat=True)

    return RolePermission.objects.filter(
        role_id__in=roles,
        permission__kode=kode_permission
    ).exists()