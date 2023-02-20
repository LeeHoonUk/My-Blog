from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from apps.models import Labels
from apps.forms.memo_forms import LabelForm


# 키워드 작성 = 로그인 시 페이지 접근 가능
@login_required
def label_create(request):

    nav_check = "sidebar_label"

    form = LabelForm()

    labels = Labels.objects.all()

    return render(request, "label/create.html", {"form" : form, "labels" : labels, "nav_check" : nav_check})

# 키워드 항목 = 로그인 시 삭제 가능
def label_list(request):

    nav_check = "sidebar_label"

    page = int(request.GET.get("p", 1))

    label_paginator = Paginator(Labels.objects.order_by("-created_at"), 10)
    labels = label_paginator.get_page(page)

    return render(request, "label/list.html", {"labels": labels, "nav_check": nav_check})