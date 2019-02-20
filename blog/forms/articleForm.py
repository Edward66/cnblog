"""
文章提交验证
"""

from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label='标题',
        error_messages={
            'max_length': "标题不能超过50个字符",
            "required": "标题不能为空",
        },
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    content = forms.CharField(
        label='内容',
        error_messages={
            "required": "内容不能为空",
        },
        widget=forms.widgets.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )


