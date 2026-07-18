from django.db import models
import os
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings



# Create your models here.
# HRIS Project
# Data Master Proyek

"""
PROJECT
"""


class JobOrder(models.Model):
    NomorJO = models.CharField(max_length=256)
    SalesOrder = models.CharField(max_length=256)
    Client = models.CharField(max_length=256, null=True, blank=True)
    Deskripsi = models.CharField(max_length=256)
    Nilai = models.FloatField()
    Invoice = models.FloatField()
    Status = models.CharField(max_length=56)
    Margin = models.FloatField()
    Persen = models.FloatField()
    StartWork = models.DateField()
    EndWork = models.DateField()
    TerminPembayaran = models.CharField(max_length=56)
    FileKontrak = models.FileField(
        upload_to="File/Project/JobOrder", null=True, blank=True
    )
    FileBudget = models.FileField(
        upload_to="File/Project/Budget", null=True, blank=True)

    def __str__(self):
        return f"{self.NomorJO} - {self.Deskripsi}"


class WorkCompletion(models.Model):
    NomorWorkCompletion = models.CharField(max_length=256)
    NomorJO = models.ForeignKey(JobOrder, on_delete=models.CASCADE)
    Tanggal = models.DateField()
    Jenis = models.CharField(max_length=56)
    Remarks = models.CharField(max_length=128)
    Nilai = models.FloatField()
    FileBA = models.FileField(
        upload_to="File/Project/WorkCompletion", null=True, blank=True
    )

    def __str__(self):
        return f"{self.NomorJO}-{self.NomorWorkCompletion}"
    
class BudgetItem(models.Model):
    project = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='budget_items',null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255)
    total_price = models.FloatField(default=0)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.project.NomorJO} - {self.name}"

class ProposedBudget(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    NomorProposedBudget = models.CharField(max_length=256,unique=True)
    NomorJO = models.ForeignKey(JobOrder, on_delete=models.CASCADE)
    Tanggal = models.DateField()
    Remarks = models.CharField(max_length=128)
    Nilai = models.FloatField()
    FileProposedBudget = models.FileField(
        upload_to="File/Project/ProposedBudget", null=True, blank=True
    )
    # Approval fields
    Submittedby = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_proposebudgets')
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    Approvedby = models.CharField(max_length=56)
    approved_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.NomorJO}-{self.NomorProposedBudget}"

class ItemProposedBudget(models.Model):
    NomorProposedBudget = models.ForeignKey(ProposedBudget, on_delete=models.CASCADE, related_name='items')
    Item = models.CharField(max_length=256)
    Jumlah = models.FloatField()
    Satuan = models.CharField(max_length=25, null=True, blank=True)
    Harga = models.FloatField()
    TotalHarga = models.FloatField()
    Remarks = models.CharField(max_length=128, blank=True,null=True)
    

    def __str__(self):
        return f"{self.NomorProposedBudget} - {self.Item}"


class ProposeBudgetApproval(models.Model):
    propose = models.ForeignKey(ProposedBudget, on_delete=models.CASCADE, related_name='approvals')

    approver = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=20)
    # pending, approved, rejected

    note = models.TextField(blank=True, null=True)

    approved_at = models.DateTimeField(null=True, blank=True)

class CashExpenseReport(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    NomorCashReport = models.CharField(max_length=256, unique=True)
    NomorProposedBudget = models.ForeignKey(ProposedBudget, on_delete=models.CASCADE)
    Tanggal = models.DateField()
    Remarks = models.CharField(max_length=128)
    Nilai = models.FloatField()
    FileCashReport = models.FileField(
        upload_to="File/Project/CashReport", null=True, blank=True
    )
        # Approval fields
    Submittedby = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_cash_reports')
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    Approvedby = models.CharField(max_length=56,null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    costcode = models.ForeignKey(BudgetItem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.NomorProposedBudget}-{self.NomorCashReport}"
    
class ItemCashExpenseReport(models.Model):
    NomorCashReport = models.ForeignKey(CashExpenseReport, on_delete=models.CASCADE, related_name='items')
    Item = models.CharField(max_length=256)
    Jumlah = models.FloatField()
    Harga = models.FloatField()
    Satuan = models.CharField(max_length=25, null=True, blank=True)

    TotalHarga = models.FloatField()
    Remarks = models.CharField(max_length=128, blank=True,null=True)
    costcode = models.ForeignKey(BudgetItem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.NomorCashReport} - {self.Item}"
    
class CashExpenseReportApproval(models.Model):
    cashexpensereport = models.ForeignKey(CashExpenseReport, on_delete=models.CASCADE, related_name='approvals')

    approver = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=20)
    # pending, approved, rejected

    note = models.TextField(blank=True, null=True)

    approved_at = models.DateTimeField(null=True, blank=True)

class Invoice(models.Model):
    Tanggal = models.DateField()
    NomorInvoice = models.CharField(max_length=256, unique=True)
    NomorWorkCompletion = models.ForeignKey(WorkCompletion, on_delete=models.CASCADE)
    Nilai = models.FloatField()
    FileInvoice = models.FileField(
        upload_to="File/Project/Invoice", null=True, blank=True
    )
    Status = models.CharField(max_length=56)

    def __str__(self):
        return f"{self.NomorWorkCompletion}-{self.NomorInvoice}"

class ProjectDocuments(models.Model):
    Project = models.ForeignKey(JobOrder, on_delete=models.CASCADE)
    Tipe = models.CharField(max_length=100)
    Nomor = models.CharField(max_length=100)
    Tanggal = models.DateField()
    Deskripsi = models.CharField(max_length=255)
    File = models.FileField(upload_to="File/Project/Documents", null=True, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Last_modified_at = models.DateTimeField(auto_now=True)
    Last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_project_documents')

    def __str__(self):
        return f"{self.Project.NomorJO} - {self.Tipe} - {self.Nomor}"


"""
HRIS MODELS
"""


def rename_ktp(instance, filename):
    ext = filename.split(".")[-1]
    nama = slugify(instance.Nama)  # agar rapi dan bebas spasi
    filename = f"KTP_{nama}.{ext}"
    return os.path.join("ktp_images", filename)


def rename_npwp(instance, filename):
    ext = filename.split(".")[-1]
    nama = slugify(instance.Nama)
    filename = f"NPWP_{nama}.{ext}"
    return os.path.join("npwp_images", filename)


def rename_kk(instance, filename):
    ext = filename.split(".")[-1]
    nama = slugify(instance.Nama)
    filename = f"KK_{nama}.{ext}"
    return os.path.join("kk_images", filename)


def pasfoto(instance, filename):
    ext = filename.split(".")[-1]
    nama = slugify(instance.Nama)
    filename = f"Foto_{nama}.{ext}"
    return os.path.join("kk_images", filename)


# Data Master Project
class Proyek(models.Model):
    Nama = models.CharField(max_length=250, null=True, blank=True)
    Lokasi = models.CharField(max_length=250, blank=True, null=True)
    Deskripsi = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(f"{self.Nama} - {self.Lokasi}")


# Data Master Karyawan
class MasterJenisKaryawan(models.Model):
    JenisKaryawan = models.CharField(max_length=25)

    def __str__(self):
        return str(self.JenisKaryawan)


class MasterKaryawan(models.Model):
    Nama = models.CharField(max_length=256)
    NIK = models.CharField(max_length=256, blank=True, null=True)
    Alamat = models.CharField(max_length=256, blank=True, null=True)
    Kontak = models.IntegerField(blank=True, null=True)
    NPWP = models.CharField(max_length=256, blank=True, null=True)
    NOKK = models.CharField(max_length=256, blank=True, null=True)
    Nama_Bank = models.CharField(max_length=256, blank=True, null=True)
    NoRekening = models.CharField(max_length=256, blank=True, null=True)
    NamaIbu = models.CharField(max_length=256, blank=True, null=True)
    Remarks = models.CharField(max_length=256, blank=True, null=True)
    Status = models.CharField(max_length=256, blank=True, null=True)
    FotoKTP = models.ImageField(upload_to=rename_ktp, null=True, blank=True)
    FotoKK = models.ImageField(upload_to=rename_kk, null=True, blank=True)
    FotoNPWP = models.ImageField(upload_to=rename_npwp, null=True, blank=True)
    Gender = models.BooleanField(default=True)
    JenisKaryawan = models.ForeignKey(
        MasterJenisKaryawan, on_delete=models.CASCADE, null=True, blank=True
    )
    PasFoto = models.ImageField(upload_to=pasfoto, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,related_name='karyawan_profile')
    Role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.Nama)


class Kontrak(models.Model):

    NomerKontrak = models.CharField(max_length=256, null=True, blank=True)
    Nama = models.ForeignKey(MasterKaryawan, on_delete=models.CASCADE)
    JenisKontrak = models.CharField(max_length=250, null=True, blank=True)
    Durasi = models.IntegerField(default=0)
    TanggalAwal = models.DateField()
    TanggalAkhir = models.DateField()
    Remarks = models.CharField(max_length=50, null=True, blank=True)
    StatusAktif = models.BooleanField(default=False)
    File = models.FileField(upload_to="File/HRIS/Kontrak", null=True, blank=True)
    Proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, null=True, blank=True)
    Posisi = models.CharField(max_length=250, null=True, blank=True)
    JobOrder = models.ForeignKey(
        JobOrder, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(f"{self.Nama} - {self.NomerKontrak}")


class Absensi(models.Model):
    Karyawan = models.ForeignKey(MasterKaryawan, on_delete=models.CASCADE)
    Tanggal = models.DateField()
    StatusHadir = models.BooleanField()
    Keterangan = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(f"{self.Karyawan} - {self.Tanggal}")


# Payroll
class PeriodePayroll(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("paid", "Paid"),
    ]
    KodePeriode = models.CharField(max_length=256)
    TanggalAwal = models.DateField()
    TanggalAkhir = models.DateField()
    TanggalPembayaran = models.DateField(null=True, blank=True)
    JenisPayroll = models.CharField(max_length=25)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    joborder = models.ForeignKey(
        JobOrder, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.KodePeriode


class detailpayroll(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("paid", "Paid"),
    ]

    Karyawan = models.ForeignKey(MasterKaryawan, on_delete=models.CASCADE)
    PeriodePayroll = models.ForeignKey(PeriodePayroll, on_delete=models.CASCADE)
    BasicSalary = models.DecimalField(max_digits=12, decimal_places=2)
    AllowanceTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    DeductionTotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    Tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    Keterangan = models.TextField(blank=True)

    def __str__(self):
        return f"{self.Karyawan} - {self.PeriodePayroll}"


class AllowanceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PayrollAllowance(models.Model):
    payroll_item = models.ForeignKey(
        detailpayroll, on_delete=models.CASCADE, related_name="allowances"
    )
    allowance_type = models.ForeignKey(AllowanceType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.allowance_type.name} - {self.amount}"


class DeductionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PayrollDeduction(models.Model):
    payroll_item = models.ForeignKey(
        detailpayroll, on_delete=models.CASCADE, related_name="deductions"
    )
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.deduction_type.name} - {self.amount}"


"""
INVENTORY MODELS
"""


def rename_fotomaterial(instance, filename):
    ext = filename.split(".")[-1]
    nama = slugify(instance.NamaItem)  # agar rapi dan bebas spasi
    filename = f"Foto_{nama}.{ext}"
    return os.path.join("Inventory/Material_images", filename)


class MasterMaterial(models.Model):
    KodeItem = models.CharField(max_length=50, unique=True)
    NamaItem = models.CharField(max_length=128)
    Satuan = models.CharField(max_length=25, null=True, blank=True)
    SpesifikasiItem = models.CharField(max_length=256)
    Stock = models.FloatField()
    IsAset = models.BooleanField()
    IsAktif = models.BooleanField()
    Foto = models.ImageField(upload_to=rename_fotomaterial, null=True, blank=True)

    def __str__(self):
        return f"{self.KodeItem} - {self.NamaItem}"


class Warehouse(models.Model):
    NamaWarehouse = models.CharField(max_length=56)
    Lokasi = models.CharField(max_length=56)
    StatusPusat = models.BooleanField()
    IsAktif = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.NamaWarehouse}"


class WareHouseTransaction(models.Model):
    tanggal = models.DateField()
    NomorTransfer = models.CharField(max_length=56, unique=True)
    WarehouseAsal = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="fromwh"
    )
    WarehouseTujuan = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="towh"
    )
    Status = models.CharField(max_length=56)
    CreatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tanggal} - {self.WarehouseAsal}"


class DetailWareHouseTransaction(models.Model):
    NomorTransfer = models.ForeignKey(WareHouseTransaction, on_delete=models.CASCADE)
    item = models.ForeignKey(MasterMaterial, on_delete=models.CASCADE)
    Jumlah = models.FloatField()


class SuratJalan(models.Model):
    Tanggal = models.DateField()
    NoSuratJalan = models.CharField(max_length=72, unique=True)
    GoodReceiveNoted = models.FileField(
        upload_to="File/Inventory/TransaksiMasuk", null=True, blank=True
    )
    JobOrder = models.ForeignKey(
        JobOrder, on_delete=models.CASCADE, null=True, blank=True
    )
    WareHouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, blank=True
    )


class StockAdjustment(models.Model):
    Tanggal = models.DateField()
    Warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    Keterangan = models.CharField(max_length=56)
    Item = models.ForeignKey(MasterMaterial, on_delete=models.CASCADE)
    Jumlah = models.FloatField()

    def __str__(self):
        return f"{self.Warehouse} {self.Item}"


class MaterialMasuk(models.Model):
    NamaItem = models.ForeignKey(MasterMaterial, on_delete=models.CASCADE)
    Jumlah = models.FloatField()
    Remarks = models.CharField(max_length=256, null=True, blank=True)
    SuratJalan = models.ForeignKey(
        SuratJalan, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.NamaItem}"


class MaterialIssueSlip(models.Model):
    Tanggal = models.DateField()
    NoMIS = models.CharField(max_length=72, unique=True)
    FileMIS = models.FileField(upload_to="File/Inventory/MIS", null=True, blank=True)
    WareHouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.NoMIS}"


class MaterialKeluar(models.Model):
    NamaItem = models.ForeignKey(MasterMaterial, on_delete=models.CASCADE)
    Jumlah = models.FloatField()
    Remarks = models.CharField(max_length=50)
    NoMIS = models.ForeignKey(MaterialIssueSlip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.NoMIS.NoMIS} - {self.NamaItem}"


'''
Account Management
'''
class Role(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


# ================= PERMISSION =================
class Permission(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nama


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)



# ================= PROJECT ACCESS =================
class Project(models.Model):
    nama = models.CharField(max_length=200)

    def __str__(self):
        return self.nama


class UserProjectAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

# ================= AUDIT LOG =================
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aksi = models.CharField(max_length=255)
    waktu = models.DateTimeField(auto_now_add=True)
    keterangan = models.TextField(null=True, blank=True)

"""
Custom Models User
"""


