from django.shortcuts import render, redirect
from django.contrib.auth import logout
from apps.forms import LoginForm, RegisterForm
from django.http.response import JsonResponse
from apps.models import Users


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

# 가입 확인
def user_check(request):
    userid = request.GET.get("userid")
    try:
        Users.objects.get(userid=userid)

        msg = '현재 등록된 아이디입니다.'
        check = 'error'

    except Exception:
        if userid == '':
            msg = '아이디를 입력해주세요'
            check = 'warning'
        elif len(userid) < 4:
            msg = '반드시 4자 이상이여야 합니다.'
            check = 'warning'
        else:
            msg = '가입 가능한 아이디입니다.'
            check = 'success'
            return JsonResponse(status=200, data=dict(msg=msg, check=check, userid=userid), safe=False)

    return JsonResponse(status=412, data=dict(msg=msg, check=check), safe=False)