from django.db import models
import os
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


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


"""
Custom Models User
"""


class User(AbstractUser):
    role = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)
    Karyawan = models.OneToOneField(
        MasterKaryawan, on_delete=models.SET_NULL, null=True, blank=True
    )
