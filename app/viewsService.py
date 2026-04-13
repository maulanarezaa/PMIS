from django.contrib.auth import get_user_model
from .models import UserRole, UserProjectAccess, AuditLog
from django.contrib.auth.models import Group



def create_user_from_karyawan(karyawan, username, password, roles, projects):
    # 1. Create user
    User = get_user_model()
    user = User.objects.create_user(
        username=username,
        password=password,
    )

    # 2. Link ke karyawan
    karyawan.user = user
    karyawan.save()

    # 3. Assign role
    for role in roles:
        UserRole.objects.create(user=user, role=role)

    # 4. Assign project
    for project in projects:
        UserProjectAccess.objects.create(user=user, project=project)

    # 5. Audit log
    AuditLog.objects.create(
        user=user,
        aksi="Create User",
        keterangan=f"User dibuat dari karyawan {karyawan.Nama}"
    )

    return user

