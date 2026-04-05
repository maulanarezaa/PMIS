from django.shortcuts import render
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required


def is_valid_image(file):
    return file.content_type in ["image/jpeg", "image/png"]


# Create your views here.


@login_required
def viewmaterial(request):
    data = models.MasterMaterial.objects.all()
    return render(request, "Inventory/datamaterial.html", {"data": data})


@login_required
def viewdetailmaterial(request, id):
    data = models.MasterMaterial.objects.get(id=id)
    materialmasuk = models.MaterialMasuk.objects.filter(NamaItem=data)
    data.materialmasuk = materialmasuk
    materialkeluar = models.MaterialKeluar.objects.filter(NamaItem=data)
    data.materialkeluar = materialkeluar
    return render(request, "Inventory/datamaterialdetail.html", {"data": data})


@login_required
def tambahdatamaterial(request):
    proyek = models.Proyek.objects.all()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # Manajemen Data Karyawan
        KodeItem = request.POST["Kode"]
        if models.MasterMaterial.objects.filter(KodeItem=KodeItem).exists():
            messages.error(request, "Kode Item telah digunakan")
            return redirect("tambahdatainventory")
        NamaItem = request.POST["Nama"]
        SpesifikasiItem = request.POST["Spesifikasi"]
        Stok = request.POST["Stok"]
        StatusAset = request.POST["StatusAset"]
        StatusAktif = request.POST["StatusAktif"]
        if StatusAktif == "True":
            StatusAktif = True
        else:
            StatusAktif = False
        if StatusAset == "True":
            StatusAset = True
        else:
            StatusAset = False

        # Ambil file upload
        FotoProduk = request.FILES.get("FotoMaterial")

        karyawanobj = models.MasterMaterial(
            KodeItem=KodeItem,
            NamaItem=NamaItem,
            SpesifikasiItem=SpesifikasiItem,
            Stock=Stok,
            IsAset=StatusAset,
            IsAktif=StatusAktif,
            Foto=FotoProduk,
        ).save()
        messages.success(request, "Data berhasil ditambahkan")

        return redirect("viewmaterial")

    return render(request, "Inventory/tambahdatamaterial.html", {"proyek": proyek})


@login_required
def editmaterial(request, id):
    data = get_object_or_404(models.MasterMaterial, pk=id)

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

    return render(request, "Inventory/editdatamaterial.html", {"data": data})


@login_required
def deletekaryawan(request, id):
    materialobject = models.MasterMaterial.objects.get(pk=id)
    materialobject.delete()
    return redirect("viewmaterial")


""" MATERIAL MASUK """


@login_required
def viewmaterialmasuk(request):
    data = models.MaterialMasuk.objects.all()
    return render(request, "Inventory/materialmasuk.html", {"data": data})


@login_required
def materialmasuk(request):
    data = models.SuratJalan.objects.all()
    return render(request, "Inventory/datamaterialmasuk.html", {"data": data})


@login_required
def tambahdatamaterialmasuk(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # print(asd)
        tanggal = request.POST["tanggal"]
        suratjalan = request.POST["SuratJalan"]
        filegrn = request.FILES.get("GRN")

        item_ids = request.POST.getlist("item_id[]")
        jumlah = request.POST.getlist("jumlah")
        remarks = request.POST.getlist("remarks")
        # Create Surat Jalan
        try:
            suratjalanobj = models.SuratJalan(
                Tanggal=tanggal, NoSuratJalan=suratjalan, GoodReceiveNoted=filegrn
            ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect(tambahdatamaterialmasuk)
        try:
            for i in zip(item_ids, jumlah, remarks):
                print(i)
                materialmasukobj = models.MaterialMasuk(
                    NamaItem=models.MasterMaterial.objects.get(id=i[0]),
                    Jumlah=i[1],
                    Remarks=i[2],
                    SuratJalan=models.SuratJalan.objects.last(),
                ).save()
            messages.success(request, "Material berhasil diinput")
            return redirect("viewmaterialmasuk")
        except Exception as e:
            messages.error(request, e)
            suratjalanobj = models.SuratJalan.objects.last()
            print(suratjalanobj)
            suratjalanobj.delete()

            # update stock

    return render(request, "Inventory/tambahdatamaterialmasuk.html")


@login_required
def detailsuratjalan(request, id):
    data = models.SuratJalan.objects.get(id=id)
    datadetail = models.MaterialMasuk.objects.filter(SuratJalan=data.id)
    print(datadetail)
    return render(
        request,
        "Inventory/datamaterialmasukdetail.html",
        {"data": data, "datadetail": datadetail},
    )


@login_required
def search_item(request):
    query = request.GET.get("q", "")
    print(query)
    items = models.MasterMaterial.objects.filter(NamaItem__icontains=query)[:10]

    data = list(items.values("id", "NamaItem", "KodeItem", "SpesifikasiItem", "Satuan"))

    return JsonResponse(data, safe=False)


@login_required
def editdatasuratjalan(request, id):
    datasuratjalan = models.SuratJalan.objects.get(id=id)
    datailsuratjalan = models.MaterialMasuk.objects.filter(SuratJalan=datasuratjalan)
    if request.method == "POST":
        print(request.POST)
        # print(asd)
        # Data Surat Jalan
        datasuratjalan.NoSuratJalan = request.POST["NoSuratJalan"]
        datasuratjalan.Tanggal = request.POST["Tanggal"]
        datasuratjalan.save()
        # Update data surat jalan
        listdetailid = request.POST.getlist("detail_id[]")
        listidmaterial = request.POST.getlist("item_id[]")
        listjumlah = request.POST.getlist("jumlah[]")
        listremarks = request.POST.getlist("remarks[]")
        for item in zip(listdetailid, listidmaterial, listjumlah, listremarks):
            # cek apakah nilainya kosong --> kalau kosong maka buat record baru
            if item[0] == "":
                detailsuratjalanobj = models.MaterialMasuk(
                    NamaItem=models.MasterMaterial.objects.get(id=item[1]),
                    Jumlah=item[2],
                    Remarks=item[3],
                    SuratJalan=datasuratjalan,
                ).save()
            else:
                datadetailmasuk = models.MaterialMasuk.objects.get(id=item[0])
                datadetailmasuk.NamaItem = models.MasterMaterial.objects.get(id=item[1])
                datadetailmasuk.Jumlah = item[2]
                datadetailmasuk.Remarks = item[3]
                datadetailmasuk.save()
        messages.success(request, "Data Berhasil Tersimpan")
        return redirect("edit_materialmasuk", id=id)
    return render(
        request,
        "Inventory/editdatasuratjalan.html",
        {"data": datasuratjalan, "datadetail": datailsuratjalan},
    )


@login_required
def materialkeluar(request):
    data = models.MaterialIssueSlip.objects.all()
    for item in data:
        detaildata = models.MaterialKeluar.objects.filter(NoMIS=item)
        item.detail = detaildata
        print(item.detail)

    return render(
        request,
        "Inventory/datamaterialkeluar.html",
        {"data": data},
    )


@login_required
def tambahdatamaterialkeluar(request):
    if request.method == "POST":
        print(request.POST)
        tanggal = request.POST["tanggal"]
        NomorMIS = request.POST["MIS"]
        filemis = request.FILES.get("MIS")

        item_ids = request.POST.getlist("item_id[]")
        jumlah = request.POST.getlist("jumlah")
        remarks = request.POST.getlist("remarks")
        # Create Surat Jalan
        try:
            MISObj = models.MaterialIssueSlip(
                Tanggal=tanggal, NoMIS=NomorMIS, FileMIS=filemis
            ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahmaterialkeluar")
        try:
            for i in zip(item_ids, jumlah, remarks):
                print(i)
                materialmasukobj = models.MaterialKeluar(
                    NamaItem=models.MasterMaterial.objects.get(id=i[0]),
                    Jumlah=i[1],
                    Remarks=i[2],
                    NoMIS=models.MaterialIssueSlip.objects.last(),
                ).save()
            messages.success(request, "Material berhasil diinput")
            return redirect("viewmaterialkeluar")
        except Exception as e:
            messages.error(request, e)
            misobj = models.MaterialIssueSlip.objects.last()
            print(misobj)
            misobj.delete()
    return render(request, "Inventory/tambahdatamaterialkeluar.html")


@login_required
def detailmis(request, id):
    data = models.MaterialIssueSlip.objects.get(id=id)
    datadetail = models.MaterialKeluar.objects.filter(NoMIS=data.id)
    print(datadetail)
    return render(
        request,
        "Inventory/datamaterialkeluardetail.html",
        {"data": data, "datadetail": datadetail},
    )


"""
STOCK ADJUSTMENT
"""


@login_required
def viewstockadjustment(request):
    data = models.StockAdjustment.objects.all()
    return render(request, "Inventory/datastockadjustment.html", {"data": data})


@login_required
def addstockadjustment(request):
    data = models.MasterMaterial.objects.all()
    return render(request, "Inventory/tambahdatastockadjustment.html")


"""WAREHOUSE"""


def viewwarehouse(request):
    data = models.Warehouse.objects.all()
    return render(request, "Inventory/datawarehouse.html", {"data": data})


def addwarehouse(request):
    if request.method == "POST":
        print(request.POST)
        warehouseobj = models.Warehouse(
            NamaWarehouse=request.POST["Nama"],
            Lokasi=request.POST["lokasi"],
            StatusPusat=request.POST["statuswarehouse"],
            IsAktif=bool(request.POST["statusaktif"]),
        ).save()
        messages.success(request, "Data Berhasil disimpan")
        return redirect("viewwarehouse")
    return render(request, "Inventory/tambahwarehouse.html")


def detailwarehouse(request, id):
    data = models.Warehouse.objects.get(id=id)
    return render(request, "Inventory/datawarehousedetail.html", {"data": data})
