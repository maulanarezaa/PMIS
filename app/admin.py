from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(models.MasterKaryawan)
admin.site.register(models.Kontrak)
admin.site.register(models.Proyek)
admin.site.register(models.Absensi)
admin.site.register(models.PeriodePayroll)
admin.site.register(models.PayrollAllowance)
admin.site.register(models.PayrollDeduction)
admin.site.register(models.MasterMaterial)
admin.site.register(models.JobOrder)
admin.site.register(models.BudgetItem)
admin.site.register(models.ProposedBudget)
admin.site.register(models.ProposeBudgetApproval)
admin.site.register(models.CashExpenseReport)
admin.site.register(models.CashExpenseReportApproval)
admin.site.register(models.WorkCompletion)
admin.site.register(models.Invoice)
admin.site.register(models.ProjectDocuments)
admin.site.register(models.VendorMaster)
admin.site.register(models.VendorQuotation)
admin.site.register(models.VendorQuotationItem)
admin.site.register(models.PurchaseOrder)
admin.site.register(models.PurchaseOrderItem)


