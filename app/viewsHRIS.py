from django.shortcuts import render
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse

# Create your views here.


def viewdashboard(request):
    data = models.MasterKaryawan.objects.all()
    print(data)
    jumlahkaryawan = data.count()
    return render(
        request, "HRIS/index.html", {"data": data, "JumlahKaryawan": jumlahkaryawan}
    )


def viewkaryawan(request):
    data = models.MasterKaryawan.objects.all()
    return render(request, "HRIS/datakaryawan.html", {"data": data})


def viewkaryawandetail(request, id):
    data = models.MasterKaryawan.objects.get(pk=id)
    historikontrak = models.Kontrak.objects.filter(Nama__id=id).order_by("-TanggalAwal")
    print(historikontrak)
    return render(
        request,
        "HRIS/datakaryawandetail.html",
        {"data": data, "datakontrak": historikontrak},
    )


def editkaryawan(request, id):
    data = get_object_or_404(models.MasterKaryawan, pk=id)

    if request.method == "POST":
        data.Nama = request.POST.get("Nama")
        data.Kontak = request.POST.get("Kontak")
        data.Alamat = request.POST.get("Alamat")
        data.NIK = request.POST.get("NIK")
        data.NPWP = request.POST.get("NPWP")
        data.NOKK = request.POST.get("NOKK")
        data.Remarks = request.POST.get("Remarks")

        if request.method == "POST":

            foto_ktp = request.FILES.get("FotoKTP")
            if foto_ktp:
                if not is_valid_image(foto_ktp):
                    messages.error(request, "File KTP harus berupa JPG atau PNG.")
                    return redirect(request.path)
                data.FotoKTP = foto_ktp

            foto_npwp = request.FILES.get("FotoNPWP")
            if foto_npwp:
                if not is_valid_image(foto_npwp):
                    messages.error(request, "File NPWP harus berupa JPG atau PNG.")
                    return redirect(request.path)
                data.FotoNPWP = foto_npwp

            foto_kk = request.FILES.get("FotoKK")
            if foto_kk:
                if not is_valid_image(foto_kk):
                    messages.error(request, "File KK harus berupa JPG atau PNG.")
                    return redirect(request.path)
                data.FotoKK = foto_kk

        data.save()
        return redirect("info_karyawan", id=id)

    return render(request, "HRIS/datakaryawanedit.html", {"data": data})


def is_valid_image(file):
    return file.content_type in ["image/jpeg", "image/png"]


def tambahdatakaryawan(request):
    proyek = models.Proyek.objects.all()
    if request.method == "POST":
        print(request.POST)
        # Manajemen Data Karyawan
        NamaKaryawan = request.POST["Nama"]
        AlamatKaryawan = request.POST["Alamat"]
        KontakKaryawan = request.POST["Kontak"]
        NIKKaryawan = request.POST["NIK"]
        NPWPKaryawan = request.POST["NPWP"]
        NOKKKaryawan = request.POST["NOKK"]
        NamaIbu = request.POST["NamaIbu"]
        RemarksKaryawan = request.POST["Remarks"]
        StatusAktif = request.POST["StatusAktif"]
        if StatusAktif == "True":
            StatusAktif = True
        else:
            StatusAktif = False

        # Ambil file upload
        foto_ktp = request.FILES.get("FotoKTP")
        foto_npwp = request.FILES.get("FotoNPWP")
        foto_kk = request.FILES.get("FotoKK")
        print(request.FILES)

        karyawanobj = models.MasterKaryawan(
            Nama=NamaKaryawan,
            NIK=NIKKaryawan,
            Alamat=AlamatKaryawan,
            Kontak=KontakKaryawan,
            NPWP=NPWPKaryawan,
            NOKK=NOKKKaryawan,
            NamaIbu=NamaIbu,
            Remarks=RemarksKaryawan,
            FotoKTP=foto_ktp,
            FotoNPWP=foto_npwp,
            FotoKK=foto_kk,
            Status=StatusAktif,
        ).save()
        # Manajemen Kontrak
        NamaKaryawanobj = models.MasterKaryawan.objects.last()
        satuankontrak = request.POST["satuan_kontrak"]
        durasikontrak = int(request.POST["JenisKontrak"])
        TanggalAwal = request.POST["TanggalAwal"]
        ProyekOBJ = models.Proyek.objects.get(pk=request.POST["Proyek"])
        Posisi = request.POST["Posisi"]
        RemarksKontrak = request.POST["RemarksKontrak"]

        if StatusAktif == "True":
            StatusAktif = True
        else:
            StatusAktif = False

        tanggal_awal_obj = datetime.strptime(TanggalAwal, "%Y-%m-%d").date()
        if satuankontrak == "Hari":
            tanggal_akhir = tanggal_awal_obj + relativedelta(days=durasikontrak)
        elif satuankontrak == "Bulan":
            tanggal_akhir = tanggal_awal_obj + relativedelta(months=durasikontrak)
        elif satuankontrak == "Tahun":
            tanggal_akhir = tanggal_awal_obj + relativedelta(years=durasikontrak)
        else:
            tanggal_akhir = tanggal_awal_obj  # fallback default

        Kontrakobj = models.Kontrak(
            Nama=NamaKaryawanobj,
            JenisKontrak=satuankontrak,
            TanggalAwal=tanggal_awal_obj,
            TanggalAkhir=tanggal_akhir,
            Remarks=RemarksKontrak,
            StatusAktif=StatusAktif,
            Proyek=ProyekOBJ,
            Posisi=Posisi,
        ).save()

    return render(request, "HRIS/tambahdatakaryawan.html", {"proyek": proyek})


def deletekaryawan(request, id):
    karyawanobj = models.MasterKaryawan.objects.get(pk=id)
    karyawanobj.delete()
    return redirect("viewkaryawan")


# Fitur Kontrak
def viewkontrak(request):
    data = models.Kontrak.objects.all()
    return render(request, "HRIS/datakontrak.html", {"data": data})


def addkontrak(request):
    datakaryawan = models.MasterKaryawan.objects.all()
    dataproyek = models.Proyek.objects.all()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        nomorkontrak = request.POST["NomorKontrak"]
        NamaKaryawan = models.MasterKaryawan.objects.get(pk=request.POST["Nama"])
        JenisKontrak = request.POST["JenisKontrak"]
        tanggalawal = request.POST["TanggalAwal"]
        Posisijabatan = request.POST["Posisi"]
        proyekobj = models.Proyek.objects.get(pk=request.POST["Proyek"])
        durasikontrak = int(request.POST["DurasiKontrak"])
        StatusAktif = request.POST["StatusAktif"]
        RemarksKontrak = request.POST["RemarksKontrak"]
        FileKontrak = request.FILES.get("FileKontrak")
        if StatusAktif == "True":
            StatusAktif = True
        else:
            StatusAktif = False
        tanggal_awal_obj = datetime.strptime(tanggalawal, "%Y-%m-%d").date()
        if JenisKontrak == "Hari":
            tanggal_akhir = tanggal_awal_obj + relativedelta(days=durasikontrak)
        elif JenisKontrak == "Bulan":
            tanggal_akhir = tanggal_awal_obj + relativedelta(months=durasikontrak)
        elif JenisKontrak == "Tahun":
            tanggal_akhir = tanggal_awal_obj + relativedelta(years=durasikontrak)
        else:
            tanggal_akhir = tanggal_awal_obj  # fallback default

        kontrakobj = models.Kontrak(
            NomerKontrak=nomorkontrak,
            Nama=NamaKaryawan,
            JenisKontrak=JenisKontrak,
            TanggalAwal=tanggal_awal_obj,
            TanggalAkhir=tanggal_akhir,
            Remarks=RemarksKontrak,
            StatusAktif=StatusAktif,
            Proyek=proyekobj,
            Posisi=Posisijabatan,
            File=FileKontrak,
        ).save()
        return redirect("viewkontrak")
    return render(
        request,
        "HRIS/tambahdatakontrak.html",
        {"datakaryawan": datakaryawan, "dataproyek": dataproyek},
    )


def editkontrak(request, id):
    datakontrak = models.Kontrak.objects.get(pk=id)
    datakontrak.TanggalAwal = datakontrak.TanggalAwal.strftime("%Y-%m-%d")
    dataproyek = models.Proyek.objects.all()
    return render(
        request,
        "HRIS/datakontrakedit.html",
        {"data": datakontrak, "dataproyek": dataproyek},
    )


def ajax_detail_karyawan(request):
    nama = request.GET.get("nama")
    try:
        karyawan = models.MasterKaryawan.objects.get(Nama=nama)
        data = {
            "Alamat": karyawan.Alamat,
            "Kontak": karyawan.Kontak,
            "NIK": karyawan.NIK,
            "NPWP": karyawan.NPWP,
            "NOKK": karyawan.NOKK,
            "NamaIbu": karyawan.NamaIbu,
            "Remarks": karyawan.Remarks,
        }
    except models.MasterKaryawan.DoesNotExist:
        data = {}
    return JsonResponse(data)


def deletekontrak(request, id):
    datakontrak = models.Kontrak.objects.get(pk=id)
    datakontrak.delete()
    return redirect("viewkontrak")


def viewattendance(request):
    data = models.Absensi.objects.all()
    for item in data:
        item.Tanggal = item.Tanggal.strftime("%Y-%m-%d")
    return render(request, "HRIS/datakehadiran.html", {"data": data})


def inputattendace(request):
    datamanpower = models.MasterKaryawan.objects.all()
    if request.method == "POST":
        print(request.POST)
        tanggal = request.POST["Tanggal"]
        listidmanpower = request.POST.getlist("Nama")
        liststatushadir = request.POST.getlist("statushadir")
        listketerangan = request.POST.getlist("keterangan")
        for nama, status, keterangan in zip(
            listidmanpower, liststatushadir, listketerangan
        ):
            absensiobj = models.Absensi(
                Karyawan=models.MasterKaryawan.objects.get(pk=nama),
                Tanggal=tanggal,
                StatusHadir=status,
                Keterangan=keterangan,
            ).save()
    return render(request, "HRIS/inputkehadiran.html", {"datamanpower": datamanpower})


def editattendance(request, id):
    dataattendance = models.Absensi.objects.get(pk=id)
    if request.method == "POST":
        print(request.POST)
        statushadir = bool(request.POST["statushadir"])
        keterangan = request.POST["keterangan"]
        dataattendance.StatusHadir = statushadir
        dataattendance.Keterangan = keterangan
        dataattendance.save()
        return redirect("viewattendance")

    return render(request, "HRIS/datakehadiranedit.html", {"data": dataattendance})


def deleteattendance(request, id):
    dataattendance = models.Absensi.objects.get(pk=id)
    dataattendance.delete()
    return redirect("viewattendance")
