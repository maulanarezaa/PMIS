from django.urls import path
from . import viewsInventory


urlpatterns = [
    path("datamaterial", viewsInventory.viewmaterial, name="viewmaterial"),
    path(
        "datamaterial/detail/<str:id>",
        viewsInventory.viewdetailmaterial,
        name="detailmaterial",
    ),
    path(
        "tambahdatainventory",
        viewsInventory.tambahdatamaterial,
        name="tambahdatainventory",
    ),
    path(
        "datamaterial/edit/<str:id>", viewsInventory.editmaterial, name="edit_material"
    ),
    path(
        "datamaterial/delete/<str:id>",
        viewsInventory.deletekaryawan,
        name="delete_material",
    ),
    path("datamaterialmasuk", viewsInventory.materialmasuk, name="viewmaterialmasuk"),
    path(
        "tambahdatamaterialmasuk",
        viewsInventory.tambahdatamaterialmasuk,
        name="tambahdatamaterialmasuk",
    ),
    path(
        "datamaterialmasuk/detail/<str:id>",
        viewsInventory.detailsuratjalan,
        name="detailsuratjalan",
    ),
    path(
        "datamaterialmasuk/edit/<str:id>",
        viewsInventory.editdatasuratjalan,
        name="edit_materialmasuk",
    ),
    path("search-item/", viewsInventory.search_item, name="search_item"),
    # Material Keluar
    path(
        "datamaterialkeluar", viewsInventory.materialkeluar, name="viewmaterialkeluar"
    ),
    path(
        "datamaterialkeluar/add",
        viewsInventory.tambahdatamaterialkeluar,
        name="tambahmaterialkeluar",
    ),
    path(
        "datamaterialkeluar/detail/<str:id>", viewsInventory.detailmis, name="detailmis"
    ),
    path(
        "stockadjustment",
        viewsInventory.viewstockadjustment,
        name="viewstockadjustment",
    ),
    path(
        "stockadjustment/add",
        viewsInventory.addstockadjustment,
        name="addstockadjustment",
    ),
    # Warehouse
    path("warehouse", viewsInventory.viewwarehouse, name="viewwarehouse"),
    path("warehouse/add", viewsInventory.addwarehouse, name="tambahwarehouse"),
    path(
        "warehouse/detail/<str:id>",
        viewsInventory.detailwarehouse,
        name="detailwarehouse",
    ),
]
