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
def viewdashboard(request):
    dataexpensereport = models.CashExpenseReportApproval.objects.filter(approver=request.user, status="Pending")
    dataproposebudget = models.ProposeBudgetApproval.objects.filter(approver=request.user, status="Pending")
    data = []
    # print(dataproposebudget[0].propose.Submittedby.karyawan_profile.Nama)
    # print(asd)
    for item in dataexpensereport:
        data.append({
            'id': item.cashexpensereport.id,
            'nomor': item.cashexpensereport.NomorCashReport,
            'jenis': 'Cash Expense Report',
            'nilai': item.cashexpensereport.Nilai,
            'notes': item.cashexpensereport.Remarks,
            'submittedby': item.cashexpensereport.Submittedby.karyawan_profile.Nama,
        })
    for item in dataproposebudget:
        data.append({
            'id': item.propose.id,
            'nomor': item.propose.NomorProposedBudget,
            'jenis': 'Propose Budget',
            'nilai': item.propose.Nilai,
            'notes': item.propose.Remarks,
            'submittedby': item.propose.Submittedby.karyawan_profile.Nama if item.propose.Submittedby and hasattr(item.propose.Submittedby, 'karyawan_profile') else item.propose.Submittedby.karyawan_profile.Nama if item.propose.Submittedby and hasattr(item.propose.Submittedby, 'karyawan_profile') else str(item.propose.Submittedby),
        })
    print(data)

    return render(request, "dashboard.html", {'data': data})
