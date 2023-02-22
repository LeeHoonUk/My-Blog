from django import forms
from apps.models import Users
from argon2 import PasswordHasher, exceptions # pip install argon2-cffi
from django.contrib.auth import login
import random

# 회원가입 Form
class RegisterForm(forms.Form):
    # 아이디, 최대 100자, 필수값, input 위젯 지정
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "userid", "class" : "form-control", "placeholder" : "아이디를 입력해주세요", 
        "autofocus" : "autofocus", "minlength" : 4
    }))

    # 비밀번호, 최대 100자, 필수값, input 패스워드 위젯 지정
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        "id" : "password", "class" : "form-control", "placeholder" : "비밀번호를 입력해주세요",
        "aria-describedby" : "password", "autocomplete" : "off", "minlength" : 4
    }))

    # 비밀번호 확인, 최대 100자, 필수값, input 패스워드 위젯 지정
    check_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        "id" : "check_password", "class" : "form-control", "placeholder" : "비밀번호를 한번 더 입력해주세요",
        "aria-describedby" : "password", "autocomplete" : "off", "minlength" : 4
    }))

    # 비밀번호 힌트, 최대 100자, 필수값, input 위젯 지정
    hint = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "hint", "class" : "form-control", "placeholder" : "가장 기억에 남는 한마디 (꼭 기억해주세요)"
    }))

    # 아이디 중복 확인, 최대 10자, 필수값, input 숨김 위젯 지정
    check = forms.CharField(max_length=10, required=True, widget=forms.HiddenInput(attrs={
        "id" : "checker", "class" : "form-control", "value" : "False"
    }))

    # 회원가입
    def save(self, request, data):
        # 데이터 지정
        user_id, pw, check_pw = data.get('user_id'), data.get('password'), data.get('check_password')
        hint, check = data.get('hint'), data.get('check')

        # 메세지, status 코드
        res = (lambda x, y, z : ('아이디 중복확인이 되지 않았습니다.', 412) if x == 'False' else (
            ('비밀번호가 일치하지 않습니다.', 422) if y != z else (('비밀번호가 4자리 이하입니다.', 412) if len(y) < 4 else ('성공', 200))
        ))(check, pw, check_pw)

        # 성공 시 회원가입 후 로그인 실행
        if res[1] == 200:
            user = Users(username=user_id, password=PasswordHasher().hash(pw), hint=hint, user_auth="MEMBER")
            user.save()
            login(request, user)

        return res

# 로그인 Form
class LoginForm(forms.Form):
    # 아이디, 최대 100자, 필수값, input 위젯 지정
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "userid", "class" : "form-control", "placeholder" : "아이디를 입력해주세요", "autofocus" : "autofocus"
    }))

    # 비밀번호, 최대 100자, 필수값, input 패스워드 위젯 지정
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        "id" : "password", "class" : "form-control", "placeholder" : "비밀번호를 입력해주세요",
        "aria-describedby" : "password", "autocomplete" : "off"
    }))

    # 로그인
    def login(self, request, data):
        # 데이터 지정
        user_id, pw = data.get('user_id'), data.get('password')

        # 메세지, status 코드
        res = ("올바른 유저ID와 패스워드를 입력하세요.", 422)

        try:
            # 유저 존재 확인
            user = Users.objects.get(username=user_id)
        except Users.DoesNotExist:
            pass
        else:
            # 비밀번호 확인 
            try:
                PasswordHasher().verify(user.password, pw)
            except exceptions.VerifyMismatchError:
                pass
            else:
                # 로그인
                login(request, user)
                res = ('성공', 200)

        return res

# 초기화 Form
class FindForm(forms.Form):
    # 아이디, 최대 100자, 필수값, input 위젯 지정
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "userid", "class" : "form-control", "placeholder" : "아이디를 입력해주세요", "autofocus" : "autofocus"
    }))

    # 비밀번호 힌트, 최대 100자, 필수값, input 위젯 지정
    hint = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "hint", "class" : "form-control", "placeholder" : "가장 기억에 남는 한마디 (꼭 기억해주세요)"
    }))

    # 비밀번호 초기화
    def check(self, data):
        # 데이터 지정
        user_id, hint = data.get('user_id'), data.get('hint')

        # 무작위 4자리 숫자 반환
        random_number = random.randrange(1000, 10000)

        # 메세지, status 코드
        res = ("일치하지 않습니다.", 422)
        try:
            # 유저 존재 확인
            user = Users.objects.get(username=user_id)
        except Users.DoesNotExist:
            pass
        else:
            # 비밀번호 힌트 확인
            if user.hint != hint:
                pass
            else:
                # 무작위 4자리 비밀번호 변경 후 로그인
                user.password = PasswordHasher().hash(str(random_number))
                user.save()
                res = ('성공', 200, random_number)

        return res