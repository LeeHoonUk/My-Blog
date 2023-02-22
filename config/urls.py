"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from apps.views import *

# 이미지
from django.conf import settings
from django.conf.urls.static import static

# rest_framework
from rest_framework import routers
from apps.memo.apis import *
from apps.keyword.apis import *

# router 지정
router = routers.DefaultRouter()
router.register(r'memos', MemoViewSet)
router.register(r'keywords', KeywordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # rest_framework
    path("apis/", include(router.urls)),

    # 메인 화면
    path('', index, name="index"),

    # 사용자 관련 화면
    path("user/", include("apps.user.urls")),

    # 메모 관련 화면
    path("memo/", include("apps.memo.urls")),

    # 키워드 관련 화면
    path("keyword/", include("apps.keyword.urls")),
]
if settings.DEBUG : 
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )