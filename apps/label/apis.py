from rest_framework import viewsets, permissions
from .serializers import LabelSerializer
from apps.models import Labels


# 키워드 ViewSet
class LabelViewSet(viewsets.ModelViewSet):
    # 키워드 쿼리
    queryset = Labels.objects.order_by("-created_at")
    # 키워드 Serializer
    serializer_class = LabelSerializer
    # 자격 인증 ( 로그인 시 )
    permission_classes = [permissions.IsAuthenticated]