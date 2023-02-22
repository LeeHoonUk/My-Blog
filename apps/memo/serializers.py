from rest_framework import serializers

from apps.models import Users, Memos, Keywords

# 유저 Serializer
class UserSerializer(serializers.ModelSerializer):

    # Users Model 에서 조회하고 싶은 Fields 선택
    class Meta:
        model = Users
        fields = ["username", "user_auth", "hint", "date_joined", "last_login"]

# 메모 Serializer
class MemoSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    keywords = serializers.SlugRelatedField(many=True, read_only=True, slug_field='keyword')

    # Users Model 에서 모든 Fields 선택
    class Meta:
        model = Memos
        fields = "__all__"

    # 메모 생성
    def create(self, request, data, commit=True):
        # 데이터 지정
        instance = Memos()
        instance.writer_id = request.user.id
        instance.title = data.get("title")
        instance.content = data.get("content")
        instance.img = (lambda x : None if x.get('img') == None else x['img'])(request.FILES)

        # 키워드
        keywords = request.data.getlist('keywords')
        
        if commit:
            # 메모 생성
            instance.save()

            # 키워드가 있다면 키워드 추가
            if keywords:
                list(map(lambda x : instance.keywords.add(Keywords.objects.get(pk=x)), keywords))