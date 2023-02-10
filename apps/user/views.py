from django.shortcuts import render, redirect
from django.contrib.auth import logout
from apps.forms import LoginForm, RegisterForm


# 회원가입
def register(request):

    form = RegisterForm()

    return render(request, "user/register.html", {"form" : form})

# 로그인
def login_view(request):

    form = LoginForm(request.POST)

    return render(request, "user/login.html", {"form" : form})

# 로그아웃
def logout_view(request):
    logout(request)

    return redirect("login")