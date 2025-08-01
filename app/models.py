from django.db import models
import os
from django.utils.text import slugify

# Create your models here.
# HRIS Project
# Data Master Proyek


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


# Data Master Project
class Proyek(models.Model):
    Nama = models.CharField(max_length=250, null=True, blank=True)
    Lokasi = models.CharField(max_length=250, blank=True, null=True)
    Deskripsi = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(f"{self.Nama} - {self.Lokasi}")


# Data Master Karyawan
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

    def __str__(self):
        return str(self.Nama)


class Kontrak(models.Model):

    NomerKontrak = models.CharField(max_length=256, null=True, blank=True)
    Nama = models.ForeignKey(MasterKaryawan, on_delete=models.CASCADE)
    JenisKontrak = models.CharField(max_length=250, null=True, blank=True)
    TanggalAwal = models.DateField()
    TanggalAkhir = models.DateField()
    Remarks = models.CharField(max_length=50, null=True, blank=True)
    StatusAktif = models.BooleanField(default=False)
    File = models.FileField(upload_to="File/HRIS/Kontrak", null=True, blank=True)
    Proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, null=True, blank=True)
    Posisi = models.CharField(max_length=250, null=True, blank=True)

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
