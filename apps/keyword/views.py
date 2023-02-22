from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from apps.models import Keywords
from apps.forms.memo_forms import KeywordForm


# 키워드 작성 = 로그인 시 페이지 접근 가능
@login_required
def keyword_create(request):

    # sidebar active
    nav_check = "sidebar_label"

    # 키워드 폼
    form = KeywordForm()

    # 모든 키워드 가져오기
    keywords = Keywords.objects.all()

    return render(request, "keyword/create.html", {"form" : form, "keywords" : keywords, "nav_check" : nav_check})

# 키워드 항목 = 로그인 시 삭제 가능
def keyword_list(request):

    # sidebar active
    nav_check = "sidebar_label"

    # 페이지네이션 구현
    page = int(request.GET.get("p", 1))
    keyword_paginator = Paginator(Keywords.objects.order_by("-created_at"), 10)
    keywords = keyword_paginator.get_page(page)

    return render(request, "keyword/list.html", {"keywords": keywords, "nav_check": nav_check})