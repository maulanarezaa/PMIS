from django.urls import path
from . import viewsProject


urlpatterns = [
    path("viewjoborder", viewsProject.viewjoborder, name="viewjoborder"),
    path("joborder/add", viewsProject.tambahdatajoborder, name="tambahdatajoborder"),
    path(
        "joborder/detail/<str:id>",
        viewsProject.viewdetailjoborder,
        name="detailjoborder",
    ),
    path("workcompletion", viewsProject.viewworkcompletion, name="viewworkcompletion"),
    path(
        "workcompletion/add",
        viewsProject.tambahdataworkcompletion,
        name="tambahdataworkcompletion",
    ),
    path("search-jo/", viewsProject.search_jo, name="search_jo"),
    path("search-proposebudget/", viewsProject.search_proposebudget, name="search_proposebudget"),
    # Proposed Budget
    path('proposebudget',viewsProject.viewproposebudget,name="proposebudget"),
    path('proposebudget/add',viewsProject.tambahdataproposebudget,name="tambahdataproposebudget"),
    path('proposebudget/delete/<int:id>', viewsProject.deleteproposebudget, name="deleteproposebudget"),
    path('proposebudget/detail/<int:id>', viewsProject.detailproposebudget, name="detailproposebudget"),
    path('proposebudget/edit/<int:id>', viewsProject.editproposebudget, name="editproposebudget"),
    # Cash Expense Report
    path('cashexpensereport',viewsProject.viewcashexpensereport,name="cashexpensereport"),
    path('cashexpensereport/add',viewsProject.tambahdatacashexpensereport,name="tambahdatacashexpensereport"),
    path('cashexpensereport/delete/<int:id>', viewsProject.deletecashexpensereport, name="deletecashexpensereport"),
    path('cashexpensereport/detail/<int:id>', viewsProject.detailcashexpensereport, name="detailcashexpensereport"),
    path('cashexpensereport/edit/<int:id>', viewsProject.editcashexpensereport, name="editcashexpensereport"),
    # Invoice  
    path('invoice',viewsProject.viewinvoice,name="invoice"),
    path('invoice/add',viewsProject.tambahdatainvoice,name="tambahdatainvoice"),
    path('invoice/delete/<int:id>', viewsProject.deleteinvoice, name="deleteinvoice"),
    path('invoice/detail/<int:id>', viewsProject.detailinvoice, name="detailinvoice"),
    path('invoice/edit/<int:id>', viewsProject.editinvoice, name="editinvoice"),
    path('get-workcompletion-by-jo/', viewsProject.get_workcompletion_by_jo, name='get_workcompletion_by_jo'),
    path('get-wc-detail/', viewsProject.get_wc_detail, name='get_wc_detail'),
]
