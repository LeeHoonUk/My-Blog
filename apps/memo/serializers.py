from rest_framework import serializers
from apps.models import Users, Memos, Labels

# 유저 Serializer
class UserSerializer(serializers.ModelSerializer):

    # Users Model 에서 조회하고 싶은 Fields 선택
    class Meta:
        model = Users
        fields = ["username", "user_auth", "hint", "date_joined", "last_login"]

# 메모 Serializer
class MemoSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)

    # Users Model 에서 모든 Fields 선택
    class Meta:
        model = Memos
        fields = "__all__"