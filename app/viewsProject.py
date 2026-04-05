from django.shortcuts import render
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.db.models import Count, Q, Sum, Max
from django.contrib.auth.decorators import login_required


def is_valid_image(file):
    return file.content_type in ["image/jpeg", "image/png"]


# Create your views here.


@login_required
def viewjoborder(request):
    data = models.JobOrder.objects.all()
    print(request.user)
    return render(request, "Project/datajoborder.html", {"data": data})


@login_required
def viewdetailjoborder(request, id):
    data = models.JobOrder.objects.get(id=id)
    workcompletion = models.WorkCompletion.objects.filter(NomorJO=data)
    data.workcompletion = workcompletion
    data.totalworkcompletion = workcompletion.aggregate(Total=Sum("Nilai"))["Total"]
    subquery = (
        models.Kontrak.objects.filter(JobOrder=data)
        .values("Nama__NIK")
        .annotate(latest_id=Max("id"))
        .values("latest_id")
    )

    data.manpower = models.Kontrak.objects.filter(id__in=subquery).select_related(
        "Nama"
    )
    print(data.manpower)
    return render(request, "Project/datajoborderdetail.html", {"data": data})


@login_required
def tambahdatajoborder(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # print(asd)
        nomorjo = request.POST["nomorjo"]
        if models.JobOrder.objects.filter(NomorJO=nomorjo).exists():
            messages.error(request, "Kode Job Order telah digunakan")
            return redirect("tambahdatajoborder")
        client = request.POST["Client"]
        salesorder = request.POST["salesorder"]
        deskripsi = request.POST["deskripsi"]
        nilai = request.POST["nilai"]
        startdate = request.POST["startdate"]
        enddate = request.POST["enddate"]
        termin = request.POST["termin"]
        filekontrak = request.FILES.get("FileKontrak")
        # save data JO
        datajoobj = models.JobOrder(
            NomorJO=nomorjo,
            SalesOrder=salesorder,
            Client=client,
            Deskripsi=deskripsi,
            Nilai=nilai,
            Invoice=0,
            Status="",
            Margin=0,
            Persen=0,
            StartWork=startdate,
            EndWork=enddate,
            TerminPembayaran=termin,
            FileKontrak=filekontrak,
        ).save()
        messages.success(request, "Data Berhasil disimpan")
        return redirect("viewjoborder")
    return render(request, "Project/tambahdatajoborder.html")


@login_required
def viewworkcompletion(request):
    data = models.WorkCompletion.objects.all()
    return render(request, "Project/dataworkcompletion.html", {"data": data})


@login_required
def tambahdataworkcompletion(request):
    dataJO = models.JobOrder.objects.all()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # save object
        nowc = request.POST["nomorworkcompletion"]
        idjo = request.POST["idjo"]
        tanggal = request.POST["tanggal"]
        jenistagihan = request.POST["jenistagihan"]
        nilaitagihan = request.POST["nilaitagihan"]
        remarks = request.POST["remarks"]
        fileBA = request.FILES.get("fileba")

        # cek nomor WC
        if models.WorkCompletion.objects.filter(NomorWorkCompletion=nowc).exists():
            messages.error(request, "Nomor Work Completion sudah ada dalam sistem")
            return redirect("tambahdataworkcompletion")
        try:
            dataobj = models.WorkCompletion(
                NomorWorkCompletion=nowc,
                NomorJO=models.JobOrder.objects.get(id=idjo),
                Tanggal=tanggal,
                Jenis=jenistagihan,
                Remarks=remarks,
                Nilai=nilaitagihan,
                FileBA=fileBA,
            ).save()
            messages.success(request, "Data Berhasil disimpan")
            return redirect("viewworkcompletion")
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahdataworkcompletion")

    return render(request, "Project/tambahdataworkcompletion.html", {"datajo": dataJO})


@login_required
def search_jo(request):
    query = request.GET.get("q", "")
    results = models.JobOrder.objects.filter(
        Q(NomorJO__icontains=query) | Q(Deskripsi__icontains=query)
    )[:10]
    data = []
    for jo in results:
        data.append(
            {
                "idjo": jo.id,
                "NomorJO": jo.NomorJO,
                "SalesOrder": jo.SalesOrder,
                "Deskripsi": jo.Deskripsi,
                "Nilai": f"{int(jo.Nilai):,}".replace(",", "."),
            }
        )
    return JsonResponse(data, safe=False)
