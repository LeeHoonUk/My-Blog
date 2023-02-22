from rest_framework import serializers

from apps.models import Keywords


# 키워드 Serializer
class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keywords
        fields = "__all__"

    # 라벨 생성
    def create(self, data, commit=True):
        # 데이터 지정
        instance = Keywords()
        instance.keyword = data.get("keyword")

        if commit:
            try:
                # iexac = 같은 문자열 찾기 (대소문자 구분하지 않음)
                Keywords.objects.get(keyword__iexact=data.get("keyword"))                
            except:
                # 라벨 생성
                instance.save()
            else:
                # 중복 오류
                msg = '이미 등록된 키워드입니다.'
                return msg

        return instance