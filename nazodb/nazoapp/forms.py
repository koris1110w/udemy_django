from django import forms  

class UserForm(forms.Form):  
    username = forms.CharField(max_length=150, label="username", help_text="ユーザー名")  
    password = forms.CharField(max_length=150, label="password", help_text="パスワード")  