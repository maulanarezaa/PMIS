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
]
