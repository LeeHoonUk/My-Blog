from django.test import TestCase, Client
from apps.models import Users
from argon2 import PasswordHasher


# 회원 Test Code 작성
class AuthTestCase(TestCase):
    def setUp(self):
        Users.objects.create(
            username="Test_User",
            password=PasswordHasher().hash("1234"),
            hint="answer",
            user_auth="MEMBER")

    # 아이디 중복확인 Test
    def test_idcheck(self):
        c = Client()

        # 아이디를 입력하지 않았을 시
        request = c.post("/user/check?userid=")
        self.assertEqual(request.status_code, 412)

        # 아이디의 길이가 4자리 미만인 경우
        request = c.post("/user/check?userid="+'abc')
        self.assertEqual(request.status_code, 412)

        # 아이디가 이미 존재하는 경우
        request = c.post("/user/check?userid="+'Test_User')
        self.assertEqual(request.status_code, 412)

        # 정상입력 아이디
        request = c.post("/user/check?userid="+'Success')
        self.assertEqual(request.status_code, 200)

    # 회원가입 Test
    def test_register(self):
        c = Client()

        # 중복확인 실패 시
        body = {"user_id": "test", "password": "1234",
                "check_password": "1234", "hint": "answer", "check": "False"}
        request = c.post("/user/register", body)

        self.assertEqual(request.status_code, 412)

        # 비밀번호 4자리 미만인 경우
        body = {"user_id": "test", "password": "12",
                "check_password": "12", "hint": "answer", "check": "True"}
        request = c.post("/user/register", body)

        # 비밀번호 매칭 오류
        body = {"user_id": "test", "password": "12345",
                "check_password": "1234", "hint": "answer", "check": "True"}
        request = c.post("/user/register", body)

        self.assertEqual(request.status_code, 412)

        # 회원가입 성공!
        body = {"user_id": "tester", "password": "1234",
                "check_password": "1234", "hint": "answer", "check": "True"}
        request = c.post("/user/register", body)

        self.assertEqual(request.status_code, 200)

    # 로그인 Test
    def test_login(self):
        c = Client()

        # 아이디 비밀번호 일치하지 않음
        body = {"user_id": "Test_User", "password": "12344"}
        request = c.post("/user/login", body)

        self.assertEqual(request.status_code, 412)

        # 로그인 성공
        body = {"user_id": "Test_User", "password": "1234"}
        request = c.post("/user/login", body)

        self.assertEqual(request.status_code, 302)