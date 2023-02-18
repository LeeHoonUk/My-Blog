from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.models import Labels
from apps.forms.memo_forms import *


# 메모 작성 = 로그인 시 페이지 접근 가능
@login_required
def memo_create(request):

    nav_check = "sidebar_memo"

    form = MemoForm()

    labels = Labels.objects.all()

    return render(request, "memo/create.html", {"form": form, "labels": labels, "nav_check": nav_check})