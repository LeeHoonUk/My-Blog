from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser 사용
class Users(AbstractUser):
    user_auth = models.CharField(max_length=50) # 문자열 최대 50자
    hint = models.CharField(max_length=50) # 문자열 최대 50자

# 작성, 수정 시간을 상속
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # Date 처음 생성 시 설정
    updated_at = models.DateTimeField(auto_now=True) # Date 저장 시 설정

    # 선언함으로써, 다른 모델들이 상속 받을 수 있는 모델이 된다.
    class Meta:
        abstract = True

# 라벨 모델 생성
class Keywords(TimeStampedModel):
    keyword = models.CharField(max_length=100) # 문자열 최대 100자

# 메모 모델 생성
class Memos(TimeStampedModel):
    title = models.CharField(max_length=100) # 문자열 최대 100자
    content = models.TextField() # 큰 텍스트 필드 
    writer = models.ForeignKey(Users, on_delete=models.CASCADE) # 유저 삭제 시 메모 삭제
    like = models.BigIntegerField(default=0) # 64비트 정수 기본값 = 0

    # blank = 폼에서 비워둘 수 있음, null = Null 저장 허용
    img = models.FileField(upload_to="", blank=True, null=True) 

    # 다대다 관계, Null 허용, 폼 비움 허용
    keywords = models.ManyToManyField('Keywords', related_name='memos', blank=True)

    # 좋아요 기능
    def clicked(self):
        self.like += 1
        self.save()
        return self

