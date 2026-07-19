from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render,redirect
from . import models
from . import forms
from django.contrib import messages

User = get_user_model()


def user_list(request):

    users = User.objects.all().prefetch_related(
        'groups',
        'profile'
    )

    context = {

        "users": users

    }

    return render(
        request,
        "Account/Userlist.html",
        context
    )

def user_create(request):

    form = forms.UserCreateForm(request.POST or None)

    employees = models.MasterKaryawan.objects.filter(
        user__isnull=True
    )
    print(employees)

    if request.method == "POST":

        employee = models.MasterKaryawan.objects.get(
            id=request.POST["employee"]
        )

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            group = form.cleaned_data["group"]

            user.groups.add(group)

            models.UserProfile.objects.create(

                user=user,

                karyawan=employee,

                created_by=user

            )

            messages.success(
                request,
                "User berhasil dibuat."
            )

            return redirect("user_list")

    context = {

        "form": form,

        "employees": employees

    }

    return render(

        request,

        "Account/createuser.html",

        context

    )

def assign_job_order(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )


    job_orders = models.JobOrder.objects.all()


    selected_job_orders = models.UserJobOrder.objects.filter(
        user=user
    ).values_list(
        "job_order_id",
        flat=True
    )


    if request.method == "POST":


        # hapus akses lama
        models.UserJobOrder.objects.filter(
            user=user
        ).delete()


        # insert akses baru

        selected = request.POST.getlist(
            "job_orders"
        )


        for jo in selected:

            models.UserJobOrder.objects.create(
                user=user,
                job_order_id=jo,
                created_by=user
            )


        messages.success(
            request,
            "Job Order access berhasil diperbarui"
        )


        return redirect(
            "user_list"
        )


    context = {

        "user": user,

        "job_orders": job_orders,

        "selected_job_orders": selected_job_orders

    }


    return render(
        request,
        "Account/joborder.html",
        context
    )

def get_user_job_orders(user):

    if user.is_superuser:
        return models.JobOrder.objects.all()

    return models.JobOrder.objects.filter(
        user_access__user=user
    )