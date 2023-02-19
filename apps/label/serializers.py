from rest_framework import serializers

from apps.models import Labels


# 키워드 Serializer
class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Labels
        fields = "__all__"

    # 라벨 생성
    def create(self, data, commit=True):
        instance = Labels()
        instance.label = data.get("label")

        if commit:
            try:
                # iexac = 같은 문자열 찾기 (대소문자 구분하지 않음)
                Labels.objects.get(label__iexact=data.get("label"))                
            except:
                instance.save()
            else:
                msg = '이미 등록된 라벨입니다.'
                return msg

        return instance