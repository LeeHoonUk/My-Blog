from rest_framework import viewsets, permissions, status
from .serializers import MemoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http.response import Http404

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

            return Response(MemoSerializer(rtn).data, status=status.HTTP_201_CREATED)
        else:
            rtn = "유효하지 않은 정보입니다."
            
            return Response(rtn, status=status.HTTP_412_PRECONDITION_FAILED)
        
    # PUT METHOD
    def update(self, request, pk=None):

        serializer = MemoSerializer(data=request.data)

        if serializer.is_valid():
            rtn = serializer.update(request, serializer.data, pk)
            return Response(MemoSerializer(rtn).data, status=status.HTTP_201_CREATED)
        else:
            rtn = "유효하지 않은 정보입니다."
            return Response(rtn, status=status.HTTP_412_PRECONDITION_FAILED)

    # 좋아요 구현    
    @action(detail=True, methods=["get", "post"])
    def like(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk)

        if not queryset.exists():
            raise Http404
        rtn = queryset.first().clicked()
        serializer = MemoSerializer(rtn)

        return Response(serializer.data, status=status.HTTP_201_CREATED)