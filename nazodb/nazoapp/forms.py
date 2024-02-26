from django import forms  

TYPE_SET = (
    ("web", "WEB"),
    ("line", "LINE"),
)
TIME_SET = (
    ("10", "〜15分"),
    ("30", "15分〜45分"),
    ("60", "45分〜90分"),
    ("120", "90分〜180分"),
    ("300", "180分〜"),
)
LEVEL_SET = (
    ('easy', "初級"),
    ('normal', "中級"),
    ('hard', "上級"),
)

class UserForm(forms.Form):  
    username = forms.CharField(max_length=150, label="username", help_text="ユーザー名")  
    password = forms.CharField(max_length=150, label="password", help_text="パスワード") 

class FilterListForm(forms.Form):
    # type = forms.CharField(choices=TYPE_SET, max_length=10, label="type")
    # time = forms.CharField(choices=TIME_SET, max_length=10, label="time")
    # level = forms.CharField(choices=LEVEL_SET, max_length=10, label="level")
    type = forms.CharField(max_length=10, label="type")
    time = forms.CharField(max_length=10, label="time")
    level = forms.CharField(max_length=10, label="level")