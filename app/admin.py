from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.MasterKaryawan)
admin.site.register(models.Kontrak)
admin.site.register(models.Proyek)
admin.site.register(models.Absensi)
admin.site.register(models.PeriodePayroll)
admin.site.register(models.PayrollAllowance)
admin.site.register(models.PayrollDeduction)
