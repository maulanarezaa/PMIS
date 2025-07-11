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
]
