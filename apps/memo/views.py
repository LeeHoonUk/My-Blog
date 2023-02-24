from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.models import Keywords, Memos
from apps.forms.memo_forms import *


# 메모 작성 = 로그인 시 페이지 접근 가능
@login_required
def memo_create(request):

    # sidebar active
    nav_check = "sidebar_memo"

    # 메모 폼
    form = MemoForm()

    # 모든 키워드 가져오기
    keywords = Keywords.objects.all()

    return render(request, "memo/create.html", {"form": form, "keywords": keywords, "nav_check": nav_check})

def memo_list(request):

    # sidebar active
    nav_check = "sidebar_memo"

    # 페이지 구현
    page = int(request.GET.get("p", 1))

    return render(request, "memo/list.html", {"nav_check": nav_check})

def memo_view(request, memo_id):

    # sidebar active
    nav_check = "sidebar_memo"

    return render(request, "memo/retrieve.html", {"nav_check": nav_check, "memo_id" : memo_id})