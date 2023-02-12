from django import forms
from apps.models import Users
from argon2 import PasswordHasher # pip install argon2-cffi
from django.contrib.auth import login

# 회원가입 Form
class RegisterForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id": "userid", "class": "form-control", "placeholder": "아이디를 입력해주세요", 
        "autofocus": "autofocus", "minlength": 4
    }))

    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        "id": "password", "class": "form-control", "placeholder": "비밀번호를 입력해주세요",
        "aria-describedby": "password", "autocomplete": "off", "minlength": 4
    }))

    check_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        "id": "check_password", "class": "form-control", "placeholder": "비밀번호를 한번 더 입력해주세요",
        "aria-describedby": "password", "autocomplete": "off", "minlength": 4
    }))

    hint = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id": "hint", "class": "form-control", "placeholder": "가장 기억에 남는 한마디를 남겨주세요 (꼭 기억해주세요)"
    }))

    check = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput(attrs={
        "id": "checker", "class": "form-control", "value": "False"
    }))

    def save(self, request, data):
        user_id, pw, check_pw = data.get('user_id'), data.get('password'), data.get('check_password')
        hint, check = data.get('hint'), data.get('check')

        res = (lambda x, y, z : ('아이디 중복확인이 되지 않았습니다.', 412) if x == 'False' else (
            ('비밀번호가 일치하지 않습니다.', 412) if y != z else (('비밀번호가 4자리 이하입니다.', 412) if len(y) < 4 else ('성공', 200))
        ))(check, pw, check_pw)
        if res[1] == 200:
            user = Users(username=user_id, password=PasswordHasher().hash(pw), hint=hint, user_auth="MEMBER")
            user.save()
            login(request, user)

        return res

# 로그인 Form
class LoginForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id": "userid", "class": "form-control", "placeholder": "아이디를 입력해주세요",
        "autofocus": "autofocus", "minlength": 4
    }))

    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        "id": "password", "class": "form-control", "placeholder": "비밀번호를 입력해주세요",
        "aria-describedby": "password", "autocomplete": "off", "minlength": 4
    }))