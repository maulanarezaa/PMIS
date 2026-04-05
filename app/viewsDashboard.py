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
    print(request.user)
    return render(request, "dashboard.html")
