"""
文章提交验证
"""

from django import forms
from blog.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = (
            'title', 'content', 'category',
        )
        labels = {
            'title': '标题',
            'content': '内容',
            'category': '分类',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {
                'max_length': "不能超过50字符",
                "required": "标题不能为空",
            },
            'content': {
                "required": "内容不能为空",
            },
            'category': {
                "required": "分类不能为空",
            },
        }


class CategoryForm(forms.Form):
    title = forms.CharField(
        max_length=32,
        label='标题',
        error_messages={
            'required': '分类不能为空',
            'max_length': "不能超过32字符",
        },
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control'},
        )

    )
