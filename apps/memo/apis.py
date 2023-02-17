from rest_framework import viewsets, permissions, status
from .serializers import MemoSerializer
from rest_framework.response import Response

from apps.models import Memos


# 메모 ViewSet
class MemoViewSet(viewsets.ModelViewSet):
    # 메모 쿼리
    queryset = Memos.objects.order_by("-created_at")
    # 메모 Serializer
    serializer_class = MemoSerializer
    # 자격 인증 ( 로그인 시 )
    permission_classes = [permissions.IsAuthenticated]