from rest_framework import serializers

from apps.models import Labels


# 키워드 Serializer
class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Labels
        fields = "__all__"