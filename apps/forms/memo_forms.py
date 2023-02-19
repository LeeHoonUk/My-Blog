from django import forms


# 메모 Form
class MemoForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "title", "class" : "form-control", "placeholder" : "제목을 입력하여 주세요",
        "autofocus" : "autofocus", "minlength" : 5, "style" : "font-size : 20px"
    }))

    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        "id" : "content", "class" : "form-control", "placeholder" : "메모 내용을 작성하여 주세요",
        "aria-label": "With textarea", "rows": "15"
    }))

    img = forms.FileField(widget=forms.FileInput(attrs={
        "id" : "formFile", "class": "form-control", "type" : "file"
    }))

# 키워드 Form
class LabelForm(forms.Form):
    label = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        "id" : "label", "class" : "form-control", "placeholder" : "키워드를 입력하여 주세요 (100자 이내)",
        "autofocus": "autofocus", 'style': 'font-size : 20px'
    }))