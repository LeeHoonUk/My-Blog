from rest_framework import viewsets, permissions, status
from .serializers import LabelSerializer
from rest_framework.response import Response

from apps.models import Labels


# 키워드 ViewSet
class LabelViewSet(viewsets.ModelViewSet):
    # 키워드 쿼리
    queryset = Labels.objects.order_by("-created_at")
    # 키워드 Serializer
    serializer_class = LabelSerializer
    # 자격 인증 ( 로그인 시 )
    permission_classes = [permissions.IsAuthenticated]

    # POST METHOD
    def create(self, request):
        
        serializer = LabelSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.create(serializer.data)
            if rtn == '이미 등록된 라벨입니다.':
                return Response(rtn, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else :
                return Response(LabelSerializer(rtn).data, status=status.HTTP_201_CREATED)
        else:
            rtn = "유효하지 않은 정보입니다."
            return Response(rtn, status=status.HTTP_422_UNPROCESSABLE_ENTITY)