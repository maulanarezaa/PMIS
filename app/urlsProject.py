from django.urls import path
from . import viewsProject


urlpatterns = [
    path("viewjoborder", viewsProject.viewjoborder, name="viewjoborder"),
    path("joborder/add", viewsProject.tambahdatajoborder, name="tambahdatajoborder"),
    path("joborder/edit/<str:id>", viewsProject.editjoborder, name="editjoborder"),
    path(
        "joborder/detail/<str:id>",
        viewsProject.viewdetailjoborder,
        name="detailjoborder",
    ),
    path(
        "joborder/detail/<str:id>/addbudget",
        viewsProject.addbudgetjofromexcel,
        name="addbudgetjofromexcel",
    ),
    path(
        "previewbulkbudget",viewsProject.preview_budget_excel,name="preview_budget_excel"
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
    # Budget
    path('budget',viewsProject.viewbudget,name="budget"),
    path('budget/add/<str:id>',viewsProject.addbudget,name="tambahdatabudget"),
    path('budget/delete/<int:id>', viewsProject.deletebudget, name="deletebudget"),
    # path('budget/detail/<int:id>', viewsProject.detailbudget, name="detailbudget"),
    path('budget/edit/<int:id>', viewsProject.editbudget, name="editbudget"),
    # Project Document
    path('projectdocuments',viewsProject.viewprojectdocuments,name="projectdocuments"),
    path('projectdocuments/add',viewsProject.tambahdataprojectdocuments,name="tambahdataprojectdocuments"),
    path('projectdocuments/delete/<int:id>', viewsProject.deleteprojectdocuments, name="deleteprojectdocuments"),
    path('projectdocuments/detail/<int:id>', viewsProject.detailprojectdocuments, name="detailprojectdocuments"),
    path('projectdocuments/edit/<int:id>', viewsProject.editprojectdocuments, name="editprojectdocuments"),
    # SUPPORT
    path("search-item/", viewsProject.searchbudget, name="searchbudet"),
    path('ajax/joborder/', viewsProject.ajax_joborder, name='ajax_joborder'),
    path('ajax/vendor/', viewsProject.ajax_vendor, name='ajax_vendor'),
    path('ajax/quotation/', viewsProject.ajax_quotation, name='ajax_quotation'),
    path('ajax/proposebudget-by-jo/', viewsProject.ajax_proposebudget_by_jo, name='ajax_proposebudget_by_jo'),
    path('ajax/budgetcostcode-by-jo/', viewsProject.ajax_budgetcostcode_by_jo, name='ajax_budgetcostcode_by_jo'),
]
