from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser 사용
class Users(AbstractUser):
    user_auth = models.CharField(max_length=50)
    hint = models.CharField(max_length=50)

# 작성, 수정 시간을 상속
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# 메모 / 라벨 모델 생성
class Labels(TimeStampedModel):
    label = models.CharField(max_length=100)

class Memos(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    writer = models.ForeignKey(Users, on_delete=models.CASCADE)
    img = models.FileField(upload_to="")
    like = models.BigIntegerField(default=0)
    labels = models.ManyToManyField('Labels', related_name='memos')