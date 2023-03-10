from rest_framework import viewsets, permissions, status
from .serializers import MemoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http.response import Http404

from apps.models import Memos
import math


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
    
    # 키워드 검색
    @action(detail=False, methods=["get", "post"])
    def search(self, request):
        
        # 키워드 및 값 받아오기
        relation = request.GET.get('relation', '내용 검색')
        key = request.GET.get('key', '')

        # 포함하는 값 쿼리
        queryset = (lambda rel, q : q(keywords__keyword__icontains=key) if rel == '키워드' else (
            q(content__icontains=key).all() if rel == '내용' else q(title__icontains=key)
        ))(relation, self.get_queryset().filter)

        # 페이지 구현
        page = int(request.GET.get("page", 1))
        page_count = math.ceil(len(queryset)/9)

        page_queryset = self.paginate_queryset(queryset)

        serializer = MemoSerializer(page_queryset, many=True)

        # 앞으로가기 / 뒤로가기
        page_next = (lambda p, pc : f"{request.path}?page={page+1}" if p < pc else None)(page, page_count)
        page_previous = (lambda p : f"{request.path}?page={page-1}" if p > 1 else None)(page)
        
        return Response({
            "count" : len(queryset), "next" : page_next, 
            "previous" : page_previous, "results" : serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["get", "post"])
    def subscribe(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk)

        if not queryset.exists():

            raise Http404

        rtn = queryset.first().subscribe(request)

        serializer = MemoSerializer(rtn)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get", "post"])
    def cancel(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk)

        if not queryset.exists():

            raise Http404

        rtn = queryset.first().cancel(request)
        
        serializer = MemoSerializer(rtn)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        