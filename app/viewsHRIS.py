from django.shortcuts import render
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.db.models import Count, Q
from .formAccount import RoleForm, PermissionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import RegisterKaryawanForm
from app.templatetags.group_tags import group_required
from django.contrib.auth.decorators import login_required
import pandas as pd

# Create your views here.

@login_required
@group_required("Project Manager","Human Resource")
def viewdashboard(request):
    data = models.MasterKaryawan.objects.all()
    print(data)
    jumlahkaryawan = data.count()
    print(request.user)
    return render(
        request, "HRIS/index.html", {"data": data, "JumlahKaryawan": jumlahkaryawan}
    )

@login_required
@group_required("Project Manager","Human Resource")
def viewkaryawan(request):
    data = models.MasterKaryawan.objects.all()
    
    return render(request, "HRIS/datakaryawan.html", {"data": data})

@login_required
@group_required("Project Manager","Human Resource")
def viewkaryawandetail(request, id):
    data = models.MasterKaryawan.objects.get(pk=id)
    historikontrak = models.Kontrak.objects.filter(Nama__id=id).order_by("-TanggalAwal")
    print(historikontrak)
    return render(
        request,
        "HRIS/datakaryawandetail.html",
        {"data": data, "datakontrak": historikontrak},
    )

@login_required
@group_required("Project Manager","Human Resource")
def register_karyawan(request, id):
    karyawan = get_object_or_404(models.MasterKaryawan, pk=id)

    # cegah kalau sudah punya akun
    if karyawan.user:
        messages.warning(request, "Karyawan sudah memiliki akun")
        return redirect('viewkaryawan')

    if request.method == 'POST':
        form = RegisterKaryawanForm(request.POST)

        if form.is_valid():
            user = form.save()

            # link ke karyawan
            karyawan.user = user
            karyawan.save()

            messages.success(request, "Akun berhasil dibuat")
            return redirect('viewkaryawan')
    else:
        # prefill username dari nama karyawan
        initial_data = {
            'username': karyawan.Nama.lower().replace(' ', '')
        }
        form = RegisterKaryawanForm(initial=initial_data)

    return render(request, 'HRIS/registerkaryawan.html', {
        'form': form,
        'karyawan': karyawan
    })

@login_required
@group_required("Project Manager","Human Resource")
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

@login_required
@group_required("Project Manager","Human Resource")
def is_valid_image(file):
    return file.content_type in ["image/jpeg", "image/png"]

@login_required
def tambahdatakaryawan(request):
    proyek = models.Proyek.objects.all()
    JobOrder = models.JobOrder.objects.all()
    if request.method == "POST":
        print(request.POST)
        # print(asdasds)
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
        penempatan = request.POST['mode_penempatan']
        if penempatan == "proyek":
            idjo = request.POST["Proyek"]
            if idjo =="":
                JobOrderobj = None
            else:
                try:
                    JobOrderobj = models.JobOrder.objects.get(pk=idjo)
                except models.JobOrder.DoesNotExist:
                    JobOrderobj = None
                    messages.error(request, "Job Order tidak ditemukan.")
        else :
            JobOrderobj = None

        if StatusAktif == "True":
            StatusAktif = True
        else:
            StatusAktif = False

        # Ambil file upload
        foto_ktp = request.FILES.get("FotoKTP")
        foto_npwp = request.FILES.get("FotoNPWP")
        foto_kk = request.FILES.get("FotoKK")
        print(request.FILES)
        if not models.MasterKaryawan.objects.filter(NIK=NIKKaryawan).exists():
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
                JenisKaryawan = penempatan,
                JobOrder=JobOrderobj
            ).save()
            # Manajemen Kontrak
            NamaKaryawanobj = models.MasterKaryawan.objects.last()
        else:
            NamaKaryawanobj = models.MasterKaryawan.objects.get(NIK=NIKKaryawan)
            messages.warning(
                request, "NIK Telah terdaftar di sistem, mendaftarkan kontrak"
            )
        satuankontrak = request.POST["satuan_kontrak"]
        durasikontrak = int(request.POST["JenisKontrak"])
        TanggalAwal = request.POST["TanggalAwal"]

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
            Posisi=Posisi,
            JobOrder=JobOrderobj,
        ).save()
        messages.success(request, "Data Berhasil Disimpan")
        return redirect("viewkaryawan")

    return render(request, "HRIS/tambahdatakaryawan.html", {"proyek": JobOrder})

def import_karyawan_excel(request):
    if request.method == "POST" and request.FILES.get("FileExcel"):
        file = request.FILES["FileExcel"]
        bulk_data =[]
        # wb = openpyxl.load_workbook(file)
        # print(wb)
        if not file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "File harus berformat .xlsx atau .xls")
            return redirect("input_karyawan")
        try:
            df = pd.read_excel(file)
            print(df)
            df = df.iloc[:, :11]  # Ambil hanya 12 kolom pertama
            df = df.dropna(how='all')
            df = df.fillna('')  # Ganti nilai NaN dengan string kosong
            print(df)
            for index, row in df.iterrows():
                if row['Jenis Karyawan'] is not "":
                    print("ini row", row['Jenis Karyawan'])
                    row['Jenis Karyawan'] = row['Jenis Karyawan'].lower()
                    if row['Jenis Karyawan'] == "office":
                        jokaryawan = None
                    else:
                        try:
                            jokaryawan = models.JobOrder.objects.get(NomorJO=row['Job Order'])
                        except models.JobOrder.DoesNotExist:
                            jokaryawan = None
                            messages.error(request, f"Job Order {row['Job Order']} tidak ditemukan.")
                            continue

                bulk_data.append(
                    models.MasterKaryawan(
                        Nama=row["Nama Karyawan"],
                        NIK=row["NIK"],
                        Alamat=row["Alamat"],
                        Kontak=row["Kontak"],
                        NPWP=row["NPWP"],
                        NOKK=row["NOKK"],
                        NamaIbu=row["Nama Ibu"],
                        Remarks=row["Remarks"],
                        JenisKaryawan=row["Jenis Karyawan"],
                        JobOrder=jokaryawan,  # Set default status aktif

                    )
                )
            models.MasterKaryawan.objects.bulk_create(bulk_data)
            messages.success(request, "Data Karyawan berhasil diimpor dari Excel")
            
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat membaca file Excel: {str(e)}")
            return redirect("viewkaryawan")
        return redirect("viewkaryawan")  # sesuaikan nama url list/form kamu

    messages.error(request, "File Excel tidak ditemukan.")
    return redirect("viewkaryawan")

@group_required("Project Manager","Human Resource")
def deletekaryawan(request, id):
    karyawanobj = models.MasterKaryawan.objects.get(pk=id)
    karyawanobj.delete()
    return redirect("viewkaryawan")


# Fitur Kontrak
@login_required
@group_required("Project Manager","Human Resource")
def viewkontrak(request):
    data = models.Kontrak.objects.all()
    return render(request, "HRIS/datakontrak.html", {"data": data})

@login_required
@group_required("Project Manager","Human Resource")
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

@login_required
@group_required("Project Manager","Human Resource")
def editkontrak(request, id):
    datakontrak = models.Kontrak.objects.get(pk=id)
    datakontrak.TanggalAwal = datakontrak.TanggalAwal.strftime("%Y-%m-%d")
    dataproyek = models.JobOrder.objects.all()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        Nomorkontrak = request.POST["NomorKontrak"]
        JenisKontrak = request.POST["JenisKontrak"]
        Durasi = request.POST["DurasiKontrak"]
        Tanggalawal = request.POST["TanggalAwal"]
        Remarks = request.POST["RemarksKontrak"]
        StatusAktif = request.POST["StatusAktif"]
        Posisi = request.POST["Posisi"]
        JobOrder = models.JobOrder.objects.get(id=request.POST["Proyek"])

        kontrakobj = models.Kontrak.objects.get(id=id)
        kontrakobj.NomerKontrak = Nomorkontrak
        kontrakobj.JenisKontrak = JenisKontrak
        kontrakobj.Durasi = Durasi
        kontrakobj.TanggalAwal = Tanggalawal
        kontrakobj.Remarks = Remarks
        kontrakobj.StatusAktif = StatusAktif
        kontrakobj.Posisi = Posisi
        kontrakobj.JobOrder = JobOrder
        kontrakobj.save()
        messages.success(request, "Data Berhasil disimpan")
        return redirect("editkontrak", id)
    return render(
        request,
        "HRIS/datakontrakedit.html",
        {"data": datakontrak, "dataproyek": dataproyek},
    )

@login_required
@group_required("Project Manager","Human Resource")
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

@login_required
@group_required("Project Manager","Human Resource")
def deletekontrak(request, id):
    datakontrak = models.Kontrak.objects.get(pk=id)
    datakontrak.delete()
    return redirect("viewkontrak")

@login_required
@group_required("Project Manager","Human Resource")
def viewattendance(request):
    data = models.Absensi.objects.all()
    for item in data:
        item.Tanggal = item.Tanggal.strftime("%Y-%m-%d")
    return render(request, "HRIS/datakehadiran.html", {"data": data})

@login_required
@group_required("Project Manager","Human Resource")
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

@login_required
@group_required("Project Manager","Human Resource")
def editattendance(request, id):
    dataattendance = models.Absensi.objects.get(pk=id)
    print(dataattendance.StatusHadir)
    if request.method == "POST":
        print(request.POST)
        statushadir = request.POST["statushadir"]
        print("ini status hadir", statushadir)
        print(bool(statushadir))
        keterangan = request.POST["keterangan"]
        dataattendance.StatusHadir = statushadir
        dataattendance.Keterangan = keterangan
        dataattendance.save()
        return redirect("viewattendance")

    return render(request, "HRIS/datakehadiranedit.html", {"data": dataattendance})

@login_required
@group_required("Project Manager","Human Resource")
def deleteattendance(request, id):
    dataattendance = models.Absensi.objects.get(pk=id)
    dataattendance.delete()
    return redirect("viewattendance")

@login_required
@group_required("Project Manager","Human Resource")
def rekapdataabsen(request):
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    data = None
    datarekap = None
    total_hadir = None
    total_tidakhadir = None
    total_karyawan = None

    if start and end:
        data = models.Absensi.objects.filter(Tanggal__range=[start, end])
        datarekap = (
            data.values("Karyawan__id", "Karyawan__Nama")
            .annotate(
                jumlah_hadir=Count("id", filter=Q(StatusHadir=True)),
                jumlah_tidakhadir=Count("id", filter=Q(StatusHadir=False)),
            )
            .order_by("Karyawan__Nama")
        )
        total_hadir = data.filter(StatusHadir=True).count()
        total_tidakhadir = data.filter(StatusHadir=False).count()
        total_karyawan = data.values("Karyawan").distinct().count()

        print(datarekap)

    context = {
        "data": data,
        "rekap": datarekap,
        "total_hadir": total_hadir,
        "total_tidakhadir": total_tidakhadir,
        "total_karyawan": total_karyawan,
    }
    return render(request, "HRIS/rekapdataabsen.html", context)

@login_required
@group_required("Project Manager","Human Resource")
def payrolllistview(request):
    data = models.PeriodePayroll.objects.all().order_by("-TanggalAwal")
    return render(request, "HRIS/payrollperiodelist.html", {"data": data})

@login_required
@group_required("Project Manager","Human Resource")
def tambahdatapayroll(request):
    if request.method == "POST":
        print(request.POST)
        kodepayroll = request.POST["KodePayroll"]
        jenis = request.POST["JenisPembayaran"]
        tanggalawal = request.POST["TanggalAwal"]
        tanggalakhir = request.POST["TanggalAkhir"]
        status = request.POST["Status"]
        joborder = request.POST['joborder']
        try:
            joborderobj = models.JobOrder.objects.get(pk=joborder)
        except models.JobOrder.DoesNotExist:
            joborderobj = None
            messages.error(request, "Job Order tidak ditemukan.")
            
        
        detailkaryawan = request.POST.getlist("karyawan[]")
        detailbasic = request.POST.getlist("BasicSalary[]")
        detailallowance = request.POST.getlist("AllowanceTotal[]")
        detaildeduction = request.POST.getlist("DeductionTotal[]")
        detailtax = request.POST.getlist("Tax[]")
        detailstatus = request.POST.getlist("Status[]")
        detailnetsalary = request.POST.getlist("NetSalary[]")

        payrollobj = models.PeriodePayroll(
            KodePeriode=kodepayroll,
            TanggalAwal=tanggalawal,
            TanggalAkhir=tanggalakhir,
            JenisPayroll=jenis,
            Status=status,
            NomorJO=joborderobj,
        ).save()
        
        for karyawan, basic, allowance, deduction, tax, status, netsalary in zip(
            detailkaryawan,
            detailbasic,
            detailallowance,
            detaildeduction,
            detailtax,
            detailstatus,
            detailnetsalary,
        ):
            models.detailpayroll(
                PeriodePayroll=models.PeriodePayroll.objects.last(),
                Karyawan=models.MasterKaryawan.objects.get(pk=karyawan),
                BasicSalary=basic,
                AllowanceTotal=allowance,
                DeductionTotal=deduction,
                Tax=tax,
                Status=status,
                NetSalary=netsalary,
                
            ).save()
        
        return redirect("payroll")
    return render(request, "HRIS/tambahdatapayrollperiode.html")

@login_required
@group_required("Project Manager","Human Resource")
def editdatapayroll(request, id):
    data = models.PeriodePayroll.objects.get(pk=id)
    if request.method == "POST":
        print(request.POST)
        kode = request.POST["KodePayroll"]
        jenis = request.POST["JenisPembayaran"]
        tanggalawal = request.POST["TanggalAwal"]
        tanggalakhir = request.POST["TanggalAkhir"]
        status = request.POST["Status"]
        data.KodePeriode = kode
        data.JenisPayroll = jenis
        data.TanggalAwal = tanggalawal
        data.TanggalAkhir = tanggalakhir
        data.Status = status
        data.save()
        return redirect("payroll")
    return render(request, "HRIS/editdatapayrollperiode.html", {"data": data})

@login_required
@group_required("Project Manager","Human Resource")
def deletepayroll(requet, id):
    data = models.PeriodePayroll.objects.get(pk=id)
    data.delete()
    return redirect("payroll")

@login_required
@group_required("Project Manager","Human Resource")
def detailpayroll(request, id):
    data = models.detailpayroll.objects.filter(PeriodePayroll__pk=id)
    data_periode = models.PeriodePayroll.objects.get(pk=id)
    return render(
        request,
        "HRIS/payrollitemlist.html",
        {"data": data, "dataperiode": data_periode},
    )


"""
Section Detail Payroll
"""

@login_required
@group_required("Project Manager","Human Resource")
def tambahdetailpayroll(request, id):
    dataperiode = models.PeriodePayroll.objects.get(pk=id)
    datakaryawan = models.MasterKaryawan.objects.all()
    if request.method == "POST":
        return redirect("payrolldetail", id=id)
    return render(
        request,
        "HRIS/tambahdetailpayroll.html",
        {"datakaryawan": datakaryawan, "dataperiode": dataperiode},
    )


'''
Support
'''
def get_karyawan(request):
    search_term = request.GET.get('q', '')  # Ambil parameter pencarian dari query string
    karyawan_list = models.MasterKaryawan.objects.filter(Nama__icontains=search_term)
    results = [{'id': karyawan.id, 'text': karyawan.Nama} for karyawan in karyawan_list]
    print("ini hasil search", results)
    return JsonResponse({'results': results})