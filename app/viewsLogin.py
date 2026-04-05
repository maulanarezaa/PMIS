from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def loginview(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # ganti sesuai halaman tujuan
        else:
            messages.error(request, "Username atau password salah")

    return render(request, "Login/auth-login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
