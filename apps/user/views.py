from django.shortcuts import render, redirect
from django.contrib.auth import logout


# 회원가입
def register(request):

    return render(request, "user/register.html")

# 로그인
def login_view(request):

    return render(request, "user/login.html")

# 로그아웃
def logout_view(request):
    logout(request)

    return redirect("login")