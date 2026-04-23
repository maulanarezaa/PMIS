from django.shortcuts import render
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.db.models import Count, Q, Sum, Max
from django.contrib.auth.decorators import login_required
from .templatetags.group_tags import group_required 
from collections import defaultdict


def is_valid_image(file):
    return file.content_type in ["image/jpeg", "image/png"]


# Create your views here.


@login_required
@group_required("Project Manager","Admin Project")
def viewjoborder(request):
    data = models.JobOrder.objects.all()
    print(request.user)
    return render(request, "Project/datajoborder.html", {"data": data})


@login_required
@group_required("Project Manager","Admin Project")
def viewdetailjoborder(request, id):
    data = models.JobOrder.objects.get(id=id)
    workcompletion = models.WorkCompletion.objects.filter(NomorJO=data)
    data.workcompletion = workcompletion
    data.totalworkcompletion = workcompletion.aggregate(Total=Sum("Nilai"))["Total"]
    data.invoice = models.Invoice.objects.filter(NomorWorkCompletion__NomorWorkCompletion__in=workcompletion.values('NomorWorkCompletion'))
    subquery = (
        models.Kontrak.objects.filter(JobOrder=data)
        .values("Nama__NIK")
        .annotate(latest_id=Max("id"))
        .values("latest_id")
    )

    data.manpower = models.Kontrak.objects.filter(id__in=subquery).select_related(
        "Nama"
    )
    proposebudget = models.ProposedBudget.objects.filter(NomorJO=data)

    for item in proposebudget:
        cer = models.CashExpenseReport.objects.filter(NomorProposedBudget=item)
        totalcer = cer.aggregate(Total=Sum("Nilai"))["Total"] or 0
        item.cer = totalcer
    
    data.proposebudget = proposebudget

    data.budgetitem = models.BudgetItem.objects.filter(project=data)
   


    # print(data.manpower)
    return render(request, "Project/datajoborderdetail.html", {"data": data})


@login_required
@group_required("Project Manager","Admin Project")
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

@group_required("Project Manager","Admin Project")
def deletejoborder(request, id):
        data = get_object_or_404(models.JobOrder, id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
        return redirect("viewjoborder")
@group_required("Project Manager","Admin Project")
def editjoborder(request, id):
    data = get_object_or_404(models.JobOrder, id=id)
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # print(asd)
        nomorjo = request.POST["nomorjo"]
        if models.JobOrder.objects.filter(NomorJO=nomorjo).exclude(id=id).exists():
            messages.error(request, "Kode Job Order telah digunakan")
            return redirect("editjoborder", id=id)
        client = request.POST["Client"]
        salesorder = request.POST["salesorder"]
        deskripsi = request.POST["deskripsi"]
        nilai = request.POST["nilai"]
        startdate = request.POST["startdate"]
        enddate = request.POST["enddate"]
        termin = request.POST["termin"]
        filekontrak = request.FILES.get("FileKontrak")
        
        try:
            data.NomorJO = nomorjo
            data.Client = client
            data.SalesOrder = salesorder
            data.Deskripsi = deskripsi
            data.Nilai = nilai
            data.StartWork = startdate
            data.EndWork = enddate
            data.TerminPembayaran = termin
            if filekontrak:
                data.FileKontrak = filekontrak
            data.save()
            messages.success(request, "Data Berhasil diupdate")
            return redirect("viewjoborder")
        except Exception as e:
            messages.error(request, e)
            return redirect("editjoborder", id=id)

    return render(request, "Project/editdatajoborder.html", {"data": data})


@login_required
@group_required("Project Manager","Admin Project")
def viewworkcompletion(request):
    data = models.WorkCompletion.objects.all()
    return render(request, "Project/dataworkcompletion.html", {"data": data})


@login_required
@group_required("Project Manager","Admin Project")
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
@group_required("Project Manager","Admin Project")
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

@login_required
@group_required("Project Manager","Admin Project")
def search_proposebudget(request):
    query = request.GET.get("q", "")
    results = models.ProposedBudget.objects.filter(
        Q(NomorProposedBudget__icontains=query) | Q(NomorJO__NomorJO__icontains=query) | Q(NomorJO__Deskripsi__icontains=query)
    )[:10]
    data = []
    for jo in results:
        data.append(
            {
                "idproposebudget": jo.id,
                "NomorProposedBudget": jo.NomorProposedBudget,
                "NomorJO": jo.NomorJO.NomorJO,
                "idjo": jo.NomorJO.id,
            }
        )
    print(results)
    return JsonResponse(data, safe=False)

@login_required
@group_required("Project Manager","Admin Project")
def viewproposebudget(request):
    data = models.ProposedBudget.objects.all()
    for item in data:
        item.totalcer = models.CashExpenseReport.objects.filter(NomorProposedBudget=item).aggregate(Total=Sum("Nilai"))["Total"] or 0
    return render(request,"Project/dataproposebudget.html", {"data": data})

@login_required
@group_required("Project Manager","Admin Project")
def tambahdataproposebudget(request):
    datajo = models.JobOrder.objects.all()

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

        # save object
        nomorproposebudget = request.POST["nomorproposebudget"]
        tanggal = request.POST["tanggal"]
        file = request.FILES.get("fileproposebudget")
        item = request.POST.getlist("item")
        jumlah = request.POST.getlist("jumlah")
        satuan = request.POST.getlist("satuan")
        harga   = request.POST.getlist("harga")
        total_harga = request.POST.getlist("total_harga")
        catatan = request.POST.getlist("catatan")

        try:
            dataobj = models.ProposedBudget(
                NomorProposedBudget=nomorproposebudget,
                NomorJO = models.JobOrder.objects.get(id=request.POST["joborder"]),
                Tanggal=tanggal,
                Remarks = request.POST["remarks"],
                Nilai = sum(int(h) for h in total_harga),
                FileProposedBudget=file,
                Submittedby=request.user.username,
                Status = "Submitted",
                
            ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahdataproposebudget")
        try:
            for item in zip(item, jumlah, satuan, harga, total_harga, catatan):
                models.ItemProposedBudget(
                    NomorProposedBudget=models.ProposedBudget.objects.last(),
                    Item=item[0],
                    Jumlah=item[1],
                    Satuan=item[2],
                    Harga=item[3],
                    TotalHarga=item[4],
                    Remarks=item[5],
                ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahdataproposebudget")
        messages.success(request, "Data Berhasil disimpan")
        return redirect("proposebudget")

    return render(request, "Project/tambahdataproposebudget.html", {"datajo": datajo})

def deleteproposebudget(request, id):
        data = get_object_or_404(models.ProposedBudget, id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
        return redirect("proposebudget")

def detailproposebudget(request, id):
    data = get_object_or_404(models.ProposedBudget, id=id)
    items = models.ItemProposedBudget.objects.filter(NomorProposedBudget=data)
    cashexpensereport = models.CashExpenseReport.objects.filter(NomorProposedBudget=data)
    cashexpensereport.totalcer = cashexpensereport.aggregate(Total=Sum("Nilai"))["Total"] or 0
    data.balance = data.Nilai-cashexpensereport.totalcer

    return render(request, "Project/dataproposebudgetdetail.html", {"data": data, "items": items, "cashexpensereport": cashexpensereport})

def editproposebudget(request, id):
    data = get_object_or_404(models.ProposedBudget, id=id)
    datajo = models.JobOrder.objects.all()
    items = models.ItemProposedBudget.objects.filter(NomorProposedBudget=data)

    if request.method == "POST":
        print(request.POST)
        # print(asd)
        # ================= HEADER =================
        nomorproposebudget = request.POST.get("nomorproposebudget")
        tanggal = request.POST.get("tanggal")
        file = request.FILES.get("file")
        catatan = request.POST.get("remarks")
        idjo = request.POST.get("idjo")
        totalnilai = 0

        # ================= VALIDASI =================
        if models.ProposedBudget.objects.filter(NomorProposedBudget=nomorproposebudget).exclude(id=id).exists():
            messages.error(request, "Kode Propose Budget telah digunakan")
            return redirect("editproposebudget", id=id)

        try:
            # ================= UPDATE HEADER =================
            data.NomorProposedBudget = nomorproposebudget
            data.NomorJO = models.JobOrder.objects.get(id=idjo)
            data.Tanggal = tanggal
            data.Remarks = catatan
            totalharga = request.POST.getlist("TotalHarga")

            for dataharga in totalharga:
                totalnilai += float(dataharga)

            if file:
                data.FileProposedBudget = file
            data.Nilai = totalnilai
            data.save()

            # ================= DETAIL =================
            iditems = request.POST.getlist("iditem")
            namas = request.POST.getlist("Nama")
            jumlahs = request.POST.getlist("Jumlah")
            satuans = request.POST.getlist("Satuan")
            hargas = request.POST.getlist("Harga")
            totals = request.POST.getlist("TotalHarga")
            remarks_list = request.POST.getlist("Remarks")
            delete_flags = request.POST.getlist("delete_flag")

            
            for i in range(len(namas)):

                iditem = iditems[i]
                nama = namas[i]
                jumlah = jumlahs[i]
                satuan = satuans[i]
                harga = hargas[i]
                total = totals[i]
                remark = remarks_list[i]
                delete_flag = delete_flags[i]

                # ================= DELETE =================
                if delete_flag == "1":
                    if iditem:
                        models.ItemProposedBudget.objects.filter(id=iditem).delete()
                    continue

                # ================= UPDATE =================
                if iditem:
                    itemobj = models.ItemProposedBudget.objects.get(id=iditem)
                else:
                    itemobj = models.ItemProposedBudget(NomorProposedBudget=data)

                itemobj.Item = nama
                itemobj.Jumlah = jumlah or 0
                itemobj.Satuan = satuan
                itemobj.Harga = harga or 0
                itemobj.TotalHarga = total or 0
                itemobj.Remarks = remark
                itemobj.save()

            messages.success(request, "Data Berhasil diupdate")
            return redirect("proposebudget")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("editproposebudget", id=id)

    return render(request, "Project/editproposebudget.html", {
        "data": data,
        "datajo": datajo,
        "items": items
    })

'''
Cash Expense Report
'''

def viewcashexpensereport(request):
    data = models.CashExpenseReport.objects.all()
    return render(request,"Project/datacashexpensereport.html", {"data": data})

def tambahdatacashexpensereport(request):
    datajo = models.JobOrder.objects.all()
    dataproposedbudget = models.ProposedBudget.objects.all()

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # print(asd)

        # save object
        nomorcer = request.POST["nomorcashexpensereport"]
        tanggal = request.POST["tanggal"]
        file = request.FILES.get("filecer")
        item = request.POST.getlist("item")
        jumlah = request.POST.getlist("jumlah")
        satuan = request.POST.getlist("satuan")
        harga   = request.POST.getlist("harga")
        total_harga = request.POST.getlist("total_harga")
        catatan = request.POST.getlist("catatan")

        try:
            dataobj = models.CashExpenseReport(
                NomorCashReport=nomorcer,
                NomorProposedBudget = models.ProposedBudget.objects.get(id=request.POST["proposebudget"]),
                Tanggal=tanggal,
                Remarks = request.POST["remarks"],
                Nilai = sum(int(h) for h in total_harga),
                FileCashReport=file,
                Submittedby=request.user.username,
                Status = "Submitted",
                
            ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahdatacashexpensereport")
        try:
            for item in zip(item, jumlah, satuan, harga, total_harga, catatan):
                models.ItemCashExpenseReport(
                    NomorCashReport=models.CashExpenseReport.objects.last(),
                    Item=item[0],
                    Jumlah=item[1],
                    Satuan=item[2],
                    Harga=item[3],
                    TotalHarga=item[4],
                    Remarks=item[5],
                ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahdatacashexpensereport")
        messages.success(request, "Data Berhasil disimpan")
        return redirect("cashexpensereport")

    return render(request, "Project/tambahdatacashexpensereport.html", {"datajo": datajo, "dataproposebudget": dataproposedbudget})

def deletecashexpensereport(request, id):
        data = get_object_or_404(models.CashExpenseReport, id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
        return redirect("cashexpensereport")

def detailcashexpensereport(request, id):
    data = get_object_or_404(models.CashExpenseReport, id=id)
    items = models.ItemCashExpenseReport.objects.filter(NomorCashReport=data)
    

    return render(request, "Project/datacashexpensereportdetail.html", {"data": data, "items": items})

def editcashexpensereport(request, id): 
    data = get_object_or_404(models.CashExpenseReport, id=id)
    dataproposedbudget = models.ProposedBudget.objects.all()
    items = models.ItemCashExpenseReport.objects.filter(NomorCashReport=data)
    costcategory = models.BudgetItem.objects.filter(project=data.NomorProposedBudget.NomorJO)
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

        # update object
        nomorcer = request.POST["nomorexpensereport"]
        tanggal = request.POST["tanggal"]
        idproposebudget = request.POST["idproposebudget"]
        catatanPB = request.POST["remarks"]
        file = request.FILES.get("file")
        catatan = request.POST.getlist("Remarksitem")
        iditem = request.POST.getlist("iditem")
        jumlah = request.POST.getlist("Jumlah")
        Satuan = request.POST.getlist("Satuan")
        Harga = request.POST.getlist("Harga")
        Nama = request.POST.getlist('Nama')
        costcodelist = request.POST.getlist('costcode[]')
        Totalharga = request.POST.getlist('TotalHarga')
        nilaitotal = 0
        print(iditem, jumlah, Satuan, Harga, Totalharga, catatan,Nama)
        if models.CashExpenseReport.objects.filter(NomorCashReport=nomorcer).exclude(id=id).exists():
            messages.error(request, "Kode Cash Expense Report telah digunakan")
            return redirect("editcashexpensereport", id=id)

        try:
            data.NomorCashReport =  nomorcer
            data.NomorProposedBudget = models.ProposedBudget.objects.get(id=idproposebudget)

            data.Tanggal = tanggal
            data.Remarks = catatanPB
            if file:
                data.FileCashReport = file
            data.save()

            for item in zip(iditem, jumlah, Satuan, Harga, Totalharga, catatan,Nama,costcodelist):
                print(item)
                if item[0] != "": # jika iditem ada, update item
                    itemobj = models.ItemCashExpenseReport.objects.get(id=item[0])
                    itemobj.Jumlah = item[1]
                    itemobj.Satuan = item[2]
                    itemobj.Harga = item[3]
                    itemobj.TotalHarga = item[4]
                    itemobj.Remarks = item[5]
                    itemobj.Item = item[6]
                    itemobj.costcode = models.BudgetItem.objects.get(id=item[7]) if item[7] else None
                    itemobj.save()
                    print('itemo')
                else: # jika iditem tidak ada, buat item baru
                    models.ItemCashExpenseReport(
                        NomorCashReport=data,
                        Jumlah=item[1],
                        Satuan=item[2],
                        Harga=item[3],
                        TotalHarga=item[4],
                        Remarks=item[5],
                        Item = item[6],
                        costcode = models.BudgetItem.objects.get(id=item[7]) if item[7] else None
                    ).save()
                    print('Masuk')

            messages.success(request, "Data Berhasil diupdate")
            data.Nilai = models.ItemCashExpenseReport.objects.filter(NomorCashReport=data).aggregate(total=Sum('TotalHarga'))['total']
            data.save()
            return redirect("cashexpensereport")
        except Exception as e:
            messages.error(request, e)
            return redirect("editcashexpensereport", id=id)

    return render(request, "Project/editcashexpensereport.html", {"data": data, "dataproposebudget": dataproposedbudget, "items": items, "costcategory": costcategory})

# Invoice Management    
def viewinvoice(request):
    data = models.Invoice.objects.all()
    return render(request,"Project/datainvoice.html", {"data": data})

def tambahdatainvoice(request):
    datajo = models.JobOrder.objects.all()

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # print(asd)

        # save object
        tanggal = request.POST["tanggal"]
        nomorinvoice = request.POST["nomorinvoice"]
        file = request.FILES.get("fileinvoice")
        

        try:
            dataobj = models.Invoice(
                Tanggal = tanggal,
                NomorInvoice=nomorinvoice,
                NomorWorkCompletion = models.WorkCompletion.objects.get(id=request.POST["workcompletion"]),
                Nilai = request.POST["nilai"],
                Status = "Unpaid",
                FileInvoice = file
            ).save()
        except Exception as e:
            messages.error(request, e)
            return redirect("tambahdatainvoice")
        messages.success(request, "Data Berhasil disimpan")
        return redirect("invoice")

    return render(request, "Project/tambahdatainvoice.html", {"datajo": datajo})

def deleteinvoice(request, id):
        data = get_object_or_404(models.Invoice, id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
        return redirect("invoice")

def detailinvoice(request, id):
    data = get_object_or_404(models.Invoice, id=id)
    items = models.ItemInvoice.objects.filter(NomorInvoice=data)

    return render(request, "Project/datainvoicedetail.html", {"data": data, "items": items})

def editinvoice(request, id):
    data = get_object_or_404(models.Invoice, id=id)
    datajo = models.JobOrder.objects.all()
    items = models.ItemInvoice.objects.filter(NomorInvoice=data)
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        # print(asd)

        # update object
        nomorinvoice = request.POST["nomorinvoice"]
        tanggal = request.POST["tanggal"]
        file = request.FILES.get("fileinvoice")
        catatan = request.POST["remarks"]
        if models.Invoice.objects.filter(NomorInvoice=nomorinvoice).exclude(id=id).exists():
            messages.error(request, "Kode Invoice telah digunakan")
            return redirect("editinvoice", id=id)


        try:
            data.NomorInvoice =  nomorinvoice
            data.NomorJO = models.JobOrder.objects.get(id=request.POST["NomorJO"])

            data.Tanggal = tanggal
            data.Remarks = catatan
            if file:
                data.FileInvoice = file
            data.save()
            messages.success(request, "Data Berhasil diupdate")
            return redirect("invoice")
        except Exception as e:
            messages.error(request, e)
            return redirect("editinvoice", id=id)

    return render(request, "Project/editinvoice.html", {"data": data, "datajo": datajo, "items": items})

from django.http import JsonResponse
from .models import WorkCompletion

def get_workcompletion_by_jo(request):
    jo_id = request.GET.get('jo_id')
    print(jo_id)
    # print(asd)

    data = list(
        WorkCompletion.objects.filter(NomorJO_id=jo_id)
        .values('id', 'NomorWorkCompletion')
    )

    return JsonResponse(data, safe=False)

def get_wc_detail(request):
    wc_id = request.GET.get('id')

    wc = WorkCompletion.objects.get(id=wc_id)

    return JsonResponse({
        'nilai': wc.Nilai
    })

'''BUDGET'''

def viewbudget(request):
    items = models.BudgetItem.objects.all()
    return render(request,"Project/budget.html", { "items": items})

def addbudget(request, id):
    datajo = models.JobOrder.objects.get(id=id)
    if request.method == "POST":
        print(request.POST)
        listcostcode = request.POST.getlist("costcode")
        listnama = request.POST.getlist("nama")
        listtotal = request.POST.getlist("total")
        listremarks = request.POST.getlist("remarks")

        try:
            for costcode, nama, total, remarks in zip(listcostcode, listnama, listtotal, listremarks):
                models.BudgetItem(
                    project = datajo,
                    code = costcode,
                    name = nama,
                    total_price = total,
                    remarks = remarks
                ).save()
            messages.success(request, "Data Berhasil disimpan")
            return redirect("budget")
        except Exception as e:
            messages.error(request, e)
            return redirect("detailjoborder", id=id)

    return render(request, "Project/addbudget.html", {"datajo": datajo})

def editbudget(request, id):
    item = get_object_or_404(models.BudgetItem, id=id)
    if request.method == "POST":
        print(request.POST)
        costcode = request.POST["costcode"]
        nama = request.POST["nama"]
        total = request.POST["total"]
        remarks = request.POST["remarks"]

        try:
            item.code = costcode
            item.name = nama
            item.total_price = total
            item.remarks = remarks
            item.save()
            messages.success(request, "Data Berhasil diupdate")
            return redirect("budget")
        except Exception as e:
            messages.error(request, e)
            return redirect("editbudget", id=id)

    return render(request, "Project/editbudget.html", {"data": item})

def deletebudget(request, id):
    item = get_object_or_404(models.BudgetItem, id=id)
    item.delete()
    messages.success(request, "Data Berhasil dihapus")
    return redirect("budget")

def searchbudget(request):
    query = request.GET.get("q", "")
    jo = request.GET.get("jo", "")
    hasil = models.BudgetItem.objects.filter(project__id=jo)
    results = hasil.filter(
        Q(name__icontains=query) | Q(code__icontains=query) | Q(project__NomorJO__icontains=query)
    )[:10]
    data = []
    for item in results:
        data.append(
            {
                "id": item.id,
                "code": item.code,
                "name": item.name,
                "total_price": f"{int(item.total_price):,}".replace(",", "."),
                "remarks": item.remarks,
                "project": item.project.NomorJO,
            }
        )
    
    # print(results)
    print(query)
    return JsonResponse(data, safe=False)