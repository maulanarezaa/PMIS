from django.urls import path
from . import viewsHRIS


urlpatterns = [
    path("", viewsHRIS.viewdashboard, name="dashboardhris"),
    # Karyawan Section
    path("datakaryawan", viewsHRIS.viewkaryawan, name="viewkaryawan"),
    path("datakaryawan/<str:id>", viewsHRIS.viewkaryawandetail, name="info_karyawan"),
    path("datakaryawan/edit/<str:id>", viewsHRIS.editkaryawan, name="edit_karyawan"),
    path("tambahdatakaryawan", viewsHRIS.tambahdatakaryawan, name="tambahdatakaryawan"),
    path(
        "datakaryawan/<str:id>/delete",
        viewsHRIS.deletekaryawan,
        name="hapusdatakaryawan",
    ),
    path(
        "datakaryawan/<str:id>/adduser",
        viewsHRIS.create_user_view,
        name="create_user_from_karyawan",
    ),
    # Kontrak Section
    path("datakontrak", viewsHRIS.viewkontrak, name="viewkontrak"),
    path("tambahdatakontrak", viewsHRIS.addkontrak, name="addkontrak"),
    path("datakontrak/edit/<str:id>", viewsHRIS.editkontrak, name="editkontrak"),
    path(
        "datakontrak/delete/<str:id>", viewsHRIS.deletekontrak, name="hapusdatakontrak"
    ),
    # Attendance Section
    path("datakehadiran", viewsHRIS.viewattendance, name="viewattendance"),
    path("inputdatakehadiran", viewsHRIS.inputattendace, name="inputattendance"),
    path("datakehadiran/edit/<str:id>", viewsHRIS.editattendance, name="editabsensi"),
    path(
        "datakehadiran/hapus/<str:id>",
        viewsHRIS.deleteattendance,
        name="deleteattendance",
    ),
    path("datakehadiran/rekap", viewsHRIS.rekapdataabsen, name="rekapdataabsen"),
    # Payroll section
    path("payroll", viewsHRIS.payrolllistview, name="payroll"),
    path("payroll/add", viewsHRIS.tambahdatapayroll, name="payrolladd"),
    path("payroll/edit/<str:id>", viewsHRIS.editdatapayroll, name="payrolledit"),
    path("payroll/delete/<str:id>", viewsHRIS.deletepayroll, name="payrolldelete"),
    path("payroll/detail/<str:id>", viewsHRIS.detailpayroll, name="payrolldetail"),
    # # Detail Payroll
    path(
        "payroll/detail/<str:id>/item",
        viewsHRIS.tambahdetailpayroll,
        name="detailpayroll",
    ),
    # ROLE
    path('role/', viewsHRIS.role_list, name='role_list'),
    path('role/add/', viewsHRIS.role_create, name='role_create'),
    path('role/edit/<int:id>/', viewsHRIS.role_edit, name='role_edit'),
    path('role/delete/<int:id>/', viewsHRIS.role_delete, name='role_delete'),

    # PERMISSION
    path('permission/', viewsHRIS.permission_list, name='permission_list'),
    path('permission/add/', viewsHRIS.permission_create, name='permission_create'),
    path('permission/edit/<int:id>/', viewsHRIS.permission_edit, name='permission_edit'),
    path('permission/delete/<int:id>/', viewsHRIS.permission_delete, name='permission_delete'),
]
