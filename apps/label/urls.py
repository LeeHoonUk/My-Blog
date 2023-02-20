from apps.label.views import *
from django.urls import path

urlpatterns = [
    # 키워드 작성
    path("write", label_create, name="l-write"),
    # 키워드 리스트
    path("list", label_list, name="l-list"),
]