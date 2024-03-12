from django import forms

TYPE_SET = (
    # ("", "選択してください"),
    ("web", "WEB"),
    ("line", "LINE"),
)
TIME_SET = (
    # ("", "選択してください"),
    ("10", "〜15分"),
    ("30", "15分〜45分"),
    ("60", "45分〜90分"),
    ("120", "90分〜180分"),
    ("300", "180分〜"),
)
LEVEL_SET = (
    # ("", "選択してください"),
    ('1', "初級"),
    ('2', "中級"),
    ('3', "上級"),
)
ORDER_SET = (
    # ("", "選択してください"),
    ('rating', "評価順"),
    ('level', "難易度順"),
    ('playings', "プレイ数順"),
)

class UserForm(forms.Form):
    username = forms.CharField(max_length=150, label="username", help_text="ユーザー名")
    password = forms.CharField(max_length=150, label="password", help_text="パスワード")


class FilterListForm(forms.Form):
    name = forms.CharField(label="検索", max_length=255, required=False, widget=forms.TextInput(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    # type = forms.ChoiceField(label="タイプ", choices=TYPE_SET, required=False, widget=forms.Select(
    #     attrs={
    #         'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
    #     }
    # ))
    # time = forms.ChoiceField(label="時間", choices=TIME_SET, required=False, widget=forms.Select(
    #     attrs={
    #         'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
    #     }
    # ))
    # level = forms.ChoiceField(label="難易度", choices=LEVEL_SET, required=False, widget=forms.Select(
    #     attrs={
    #         'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
    #     }
    # ))
    type = forms.MultipleChoiceField(label="タイプ", choices=TYPE_SET, required=False, widget=forms.CheckboxSelectMultiple(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    time = forms.MultipleChoiceField(label="時間", choices=TIME_SET, required=False, widget=forms.CheckboxSelectMultiple(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    level = forms.MultipleChoiceField(label="難易度", choices=LEVEL_SET, required=False, widget=forms.CheckboxSelectMultiple(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    order = forms.ChoiceField(label="並び替え", choices=ORDER_SET, required=False, widget=forms.Select(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))

class ReviewForm(forms.Form):
    rating = forms.IntegerField(label="評価", min_value=1, max_value=5, widget=forms.NumberInput(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    rating_story = forms.IntegerField(label="ストーリー性", min_value=1, max_value=5, widget=forms.NumberInput(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    rating_gimmick = forms.IntegerField(label="ギミック", min_value=1, max_value=5, widget=forms.NumberInput(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    rating_sukkiri = forms.IntegerField(label="スッキリ感", min_value=1, max_value=5, widget=forms.NumberInput(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))
    rating_level = forms.IntegerField(label="難易度", min_value=1, max_value=5, widget=forms.NumberInput(
        attrs={
            'class': 'peer p-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600 focus:pt-6 focus:pb-2 [&:not(:placeholder-shown)]:pt-6 [&:not(:placeholder-shown)]:pb-2 autofill:pt-6 autofill:pb-2'
        }
    ))