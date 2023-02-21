from django.test import TestCase, Client
from apps.models import Labels, Users
from argon2 import PasswordHasher


# 회원 Test Code 작성
class MemosTestCase(TestCase):
    def setUp(self):
        # 라벨 등록
        Labels.objects.create(label="Django")
        # 아이디 등록
        Users.objects.create(
            username="Test_User",
            password=PasswordHasher().hash("1234"),
            hint="answer",
            user_auth="MEMBER"
        )
    
    # 라벨 등록 Test
    def test_label(self):
        c = Client()

        # 로그인 성공
        body = {"user_id" : "Test_User", "password" : "1234"}
        c.post("/user/login", body)

        # 라벨을 입력하지 않았을 시
        body = {"label" : ""}
        request = c.post("/apis/labels/", body)

        self.assertEqual(request.status_code, 412)

        # 라벨 중복 에러
        body = {"label" : "Django"}
        request = c.post("/apis/labels/", body)

        self.assertEqual(request.status_code, 422)

        # 라벨 등록
        body = {"label" : "Flask"}
        request = c.post("/apis/labels/", body)

        self.assertEqual(request.status_code, 201)

        # 라벨 삭제
        request = c.delete("/apis/labels/2/", body)

        self.assertEqual(request.status_code, 204)