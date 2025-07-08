from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.MasterKaryawan)
admin.site.register(models.Kontrak)
admin.site.register(models.Proyek)