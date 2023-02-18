from apps.memo.views import *
from django.urls import path

urlpatterns = [
    # 메모 작성
    path("write", memo_create, name="m-write"),
    
]