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

    # POST METHOD
    def create(self, request):
        
        serializer = MemoSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            if rtn == '이미 등록된 라벨입니다.':
                return Response(rtn, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else :
                return Response(MemoSerializer(rtn).data, status=status.HTTP_201_CREATED)
        else:
            rtn = "유효하지 않은 정보입니다."
            return Response(rtn, status=status.HTTP_412_PRECONDITION_FAILED)