from apps.models import Keywords, Users, Memos
from argon2 import PasswordHasher
from rest_framework.test import APITestCase, APIClient

# 메모 Test Code 작성
class MemosTestCase(APITestCase):
    def setUp(self):
        # 키워드 등록
        Keywords.objects.create(keyword="Django")
        Keywords.objects.create(keyword="Flask")

        # 아이디 등록
        Users.objects.create(
            username="Test_User",
            password=PasswordHasher().hash("1234"),
            hint="answer",
            user_auth="MEMBER"
        )

        # 메모 등록
        Memos.objects.create(
            id=1,
            title="Test Memo",
            content="Test Content",
            writer=Users.objects.get(pk=1)
        )
        # 키워드 추가
        Memos.objects.get(pk=1).keywords.add(Keywords.objects.get(pk=1))
    
    # 키워드 Test
    def test_keyword(self):
        c = APIClient()

        # 로그인 성공
        body = {"user_id" : "Test_User", "password" : "1234"}
        c.post("/user/login", body)

        # 키워드를 입력하지 않았을 시
        body = {"keyword" : ""}
        request = c.post("/apis/keywords/", body)

        self.assertEqual(request.status_code, 412)

        # 키워드 중복 에러
        body = {"keyword" : "Django"}
        request = c.post("/apis/keywords/", body)

        self.assertEqual(request.status_code, 422)

        # 키워드 등록
        body = {"keyword" : "FastAPI"}
        request = c.post("/apis/keywords/", body)

        self.assertEqual(request.status_code, 201)

        # 키워드 삭제
        request = c.delete("/apis/keywords/2/", body)

        self.assertEqual(request.status_code, 204)

    # 메모 Test
    def test_memo(self):
        c = APIClient()

        # 로그인 성공
        body = {"user_id" : "Test_User", "password" : "1234"}
        c.post("/user/login", body)

        # 제목을 입력하지 않았을 경우
        body = {"title" : "", "content" : "메모 Test"}
        request = c.post("/apis/memos/", body)

        self.assertEqual(request.status_code, 412)

        # 내용을 입력하지 않았을 경우
        body = {"title" : "메모 Test", "content" : ""}
        request = c.post("/apis/memos/", body)

        self.assertEqual(request.status_code, 412)

        # 메모 등록
        body = {"title" : "메모 Test", "content" : "매모 Test"}
        request = c.post("/apis/memos/", body)

        self.assertEqual(request.status_code, 201)

        # 메모 수정
        body = {"title" : "메모 Test", "content" : "매모 Test", "keywords" : [1, 2]}
        request = c.put("/apis/memos/1/", body)

        self.assertEqual(request.status_code, 201)

        # 메모 삭제
        request = c.delete("/apis/memos/1/", body)

        self.assertEqual(request.status_code, 204)



