from rest_framework import viewsets, permissions, status
from .serializers import KeywordSerializer
from rest_framework.response import Response

from apps.models import Keywords


# 키워드 ViewSet
class KeywordViewSet(viewsets.ModelViewSet):
    # 키워드 쿼리
    queryset = Keywords.objects.order_by("-created_at")
    # 키워드 Serializer
    serializer_class = KeywordSerializer
    # 자격 인증 ( 로그인 시 )
    permission_classes = [permissions.IsAuthenticated]

    # POST METHOD
    def create(self, request):
        
        serializer = KeywordSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.create(serializer.data)
            if rtn == '이미 등록된 키워드입니다.':
                return Response(rtn, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else :
                return Response(KeywordSerializer(rtn).data, status=status.HTTP_201_CREATED)
        else:
            rtn = "유효하지 않은 정보입니다."
            return Response(rtn, status=status.HTTP_412_PRECONDITION_FAILED)