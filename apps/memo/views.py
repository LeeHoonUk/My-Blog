from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.models import Keywords
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

# 메모 리스트 보기
def memo_list(request):

    # sidebar active
    nav_check = "sidebar_memo"

    # 페이지 구현
    page = int(request.GET.get("p", 1))

    return render(request, "memo/list.html", {"nav_check" : nav_check, 'p' : page})

# 메모 상세보기
def memo_view(request):

    # sidebar active
    nav_check = "sidebar_memo"

    if request.method == "POST":
        return render(request, "memo/retrieve.html", {
            "nav_check" : nav_check, "memo_id" : request.POST['id']
        })
    else:
        return render(request, "memo/retrieve.html", {"nav_check" : nav_check})
    
# 메모 수정 = 로그인 시 페이지 접근 가능
@login_required
def memo_update(request):

    # sidebar active
    nav_check = "sidebar_memo"

    # 모든 키워드 가져오기
    keywords = Keywords.objects.all()

    if request.method == "POST":
        return render(request, "memo/update.html", {
            "nav_check" : nav_check, "memo_id" : request.POST['id'], "keywords": keywords
        })
    else:
        return render(request, "memo/update.html", {"nav_check" : nav_check})

def memo_find(request):

    # sidebar active
    nav_check = "sidebar_memo"

    # 키워드 및 값 받아오기
    relation = request.GET.get('relation', '내용 검색')
    key = request.GET.get('key', '')

    # 페이지 구현
    page = int(request.GET.get("p", 1))

    # 모든 키워드 가져오기
    keywords = Keywords.objects.all()

    return render(request, "memo/find.html", {
        "nav_check": nav_check, "key": key, "relation": relation, 'p' : page, 'keywords' : keywords
    })