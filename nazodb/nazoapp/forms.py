from django import forms

TYPE_SET = (
    ("", "選択してください"),
    ("web", "WEB"),
    ("line", "LINE"),
)
TIME_SET = (
    ("", "選択してください"),
    ("10", "〜15分"),
    ("30", "15分〜45分"),
    ("60", "45分〜90分"),
    ("120", "90分〜180分"),
    ("300", "180分〜"),
)
LEVEL_SET = (
    ("", "選択してください"),
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
    name = forms.CharField(label="name", max_length=255, required=False, widget=forms.TextInput(
        attrs={
            'class': "bg-gray-600"
        }
    ))
    type = forms.ChoiceField(label="type", choices=TYPE_SET, required=False, widget=forms.Select(

    ))
    time = forms.ChoiceField(label="time", choices=TIME_SET, required=False, widget=forms.Select(

    ))
    level = forms.ChoiceField(label="難易度", choices=LEVEL_SET, required=False, widget=forms.Select(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
