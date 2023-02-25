from apps.memo.views import *
from django.urls import path

urlpatterns = [
    # 메모 작성
    path("write", memo_create, name="m-write"),
    # 메모 리스트
    path("list", memo_list, name="m-list"),
    # 메모 상세보기
    path("view", memo_view, name="m-view"),
]