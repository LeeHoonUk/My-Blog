from django.shortcuts import render
from apps.models import Keywords, Memos, Users
from django.core.paginator import Paginator
import datetime
from django.db.models import Count

# 메인 화면 페이지
def index(request):

    # sidebar active
    nav_check = "sidebar_main"

    # 메모 좋아요 내림차순 순서
    memo_paginator = Paginator(Memos.objects.order_by("-like"), 5)
    memo = memo_paginator.get_page(1)

    # 메모에 많이 작성된 키워드 순서
    keywords = Keywords.objects.annotate(keyword_count=Count('memos')).order_by('-keyword_count')

    # 메모를 많이 작성한 유저 순서
    user = Users.objects.annotate(user_count=Count('memos')).order_by('-user_count')
    
    # 메모, 키워드 개수
    count = (Memos.objects.all().count(), Keywords.objects.all().count())

    # 현재 날짜
    now = datetime.datetime.today()

    # 오늘 작성된 메모, 키워드, 오늘
    today = (
        Memos.objects.filter(created_at__date=now).count(),
        Keywords.objects.filter(created_at__date=now).count(),
        now
    )
    
    return render(request, "main.html", {
        "nav_check": nav_check, "count": count, "memo": memo,
        "today": today, "keywords": keywords, "best_user": user
    })