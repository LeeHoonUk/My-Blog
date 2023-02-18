from apps.label.views import *
from django.urls import path

urlpatterns = [
    # 키워드 작성
    path("write", label_create, name="l-write"),
    
]