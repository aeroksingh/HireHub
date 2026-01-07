from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.accounts.models import User
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "CANDIDATE")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            User.objects.create_user(username=username, email=email, password=password, role=role)
            messages.success(request, "Account created successfully")
            return redirect("/login/")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")
