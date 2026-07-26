from django.urls import path
from . import viewsProject


urlpatterns = [
    
    # Procurement
    path('vendorlist',viewsProject.viewvendor,name="vendorlist"),
    path('vendor/edit/<int:id>', viewsProject.editvendor, name="editvendor"),
    path('vendor/add', viewsProject.tambahvendor, name="tambahvendor"),
    path('vendor/delete/<int:id>', viewsProject.deletevendor, name="deletevendor"),
    # Quotation
    path('vendorquotation',viewsProject.vendorquotation,name="vendorquotation"),
    path('vendorquotation/add',viewsProject.tambahvendorquotation,name="tambahvendorquotation"),
    path('vendorquotation/delete/<int:id>', viewsProject.deletevendorquotation, name="deletevendorquotation"),
    path('vendorquotation/detail/<int:id>', viewsProject.detailvendorquotation, name="detailvendorquotation"),
    path('vendorquotation/edit/<int:id>', viewsProject.editvendorquotation, name="editvendorquotation"),
    # Purchase Order
    path('purchaseorder',viewsProject.purchaseorder,name="purchaseorder"),
    path('purchaseorder/add',viewsProject.tambahpurchaseorder,name="tambahpurchaseorder"),
    path('purchaseorder/detail/<int:id>', viewsProject.detailpurchaseorder, name="detailpurchaseorder"),
    path('purchaseorder/edit/<int:id>', viewsProject.editpurchaseorder, name="editpurchaseorder"),
    path('purchaseorder/delete/<int:id>', viewsProject.deletepurchaseorder, name="deletepurchaseorder"),
]
