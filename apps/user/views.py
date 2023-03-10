from django.shortcuts import render, redirect
from django.contrib.auth import logout
from apps.forms.user_forms import *
from django.http.response import JsonResponse
from apps.models import Users, Memos
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# 회원가입
def register(request):
    # POST 요청 확인
    if request.method == "POST":
        form = RegisterForm(request.POST)
        res = (lambda x : x.save(request, x.cleaned_data) if x.is_valid() else ('올바르지 않은 데이터 입니다.', 412))(form)
    else:
        form = RegisterForm()
        res = (None, 200)

    # 성공 시 메인 화면 이동
    if res[0] == '성공':
        return render(request, 'alert.html', {"first": "회원가입 완료", "second": '로그인 중 입니다.', "times": 1, 'url': "/"})
    else:
        return render(request, "user/register.html", {"form" : form, "msg": res[0]}, status=res[1])

# 로그인
def login_view(request):
    # POST 요청 확인
    if request.method == "POST":
        form = LoginForm(request.POST)
        res = (lambda x : x.login(request, x.cleaned_data) if x.is_valid() else ('올바르지 않은 데이터 입니다.', 412))(form)
    else:
        form = LoginForm()
        res = (None, 200)

    # 성공 시 메인 화면 이동
    if res[0] == '성공':
        return redirect(request.GET.get("next") or "index")
    else:
        return render(request, "user/login.html", {"form" : form, "msg": res[0]}, status=res[1])

# 로그아웃
def logout_view(request):

    logout(request)

    return redirect("login")

# 가입 확인
def user_check(request):
    userid = request.GET.get("userid")

    # 올바른 데이터 확인
    try:
        Users.objects.get(username=userid)
        res = ('현재 등록된 아이디입니다.', 'error', 422)

    except Exception:
        res = (lambda x : ('아이디를 입력해주세요', 'warning', 412) if x == '' else (
            ('반드시 4자 이상이여야 합니다.', 'warning', 412) if len(x) < 4 else ('가입 가능한 아이디입니다.', 'success', 200))
        )(userid)

    return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)

def user_find(request):
    if request.method == "POST":
        form = FindForm(request.POST)
        res = (lambda x : x.check(x.cleaned_data) if x.is_valid() else ('올바르지 않은 데이터 입니다.', 422))(form)        
    else:
        form = FindForm()
        res = (None, 200)

    # 성공 시 로그인 페이지 이동
    if res[0] == '성공':
        return render(request, 'alert.html', {
            "first": "초기화 비밀번호는 ", "second": '다음엔 꼭 기억해주세요',
            "times": 3, 'url': "login", "random_number": res[2]
        })
    else:
        return render(request, "user/find.html", {"form": form, "msg": res[0]}, status=res[1])

@login_required
def my_page(request):

    # sidebar active
    nav_check = "sidebar_main"

    # 유저 확인
    user = Users.objects.get(pk=request.user.id)

    # 페이지 구현
    page = int(request.GET.get("p", 1))

    # 내가 쓴 메모 구현
    my_memo_paginator = Paginator(
        Memos.objects.order_by("-created_at").filter(writer_id=request.user.id), 10)
    my_memo = my_memo_paginator.get_page(page)

    # 비밀번호 변경
    if request.method == "POST":
        pw = request.POST.get('password')
        
        if len(pw) < 4:
            return JsonResponse(status=412, data=dict(msg='비밀번호가 4자리 이하입니다.'), safe=False)
        else:
            user.password = PasswordHasher().hash(pw)
            user.save()
            return redirect('logout')

    return render(request, "user/mypage.html", {"nav_check": nav_check, "my_memo": my_memo})

 

    