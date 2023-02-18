from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.models import Labels
from apps.forms.memo_forms import LabelForm


# 키워드 작성 = 로그인 시 페이지 접근 가능
@login_required
def label_create(request):

    nav_check = "sidebar_label"

    form = LabelForm()

    labels = Labels.objects.all()

    return render(request, "label/create.html", {"form" : form, "labels" : labels, "nav_check" : nav_check})