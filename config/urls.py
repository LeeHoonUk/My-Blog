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

# rest_framework
from rest_framework import routers
from apps.memo.apis import *

router = routers.DefaultRouter()
router.register(r'memos', MemoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 메인 화면
    path('', index, name="index"),

    # 사용자 관련 화면
    path("user/", include("apps.user.urls")),

    # rest_framework
    path("apis/", include(router.urls)),
]
