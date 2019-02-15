"""
用户注册验证
"""
from django import forms
from django.forms import widgets, ValidationError

from blog.models import UserInfo


class RegForm(forms.Form):
    user = forms.CharField(
        max_length=32,
        min_length=6,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名长度不能超过32个',
            'min_length': '用户名长度不能少于6个',
        },
        label='用户名',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    pwd = forms.CharField(
        max_length=32,
        min_length=6,
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码长度不能超过32个',
            'min_length': '密码长度不能少于6个',
        },
        label='密码',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    re_pwd = forms.CharField(
        max_length=32,
        min_length=6,
        error_messages={
            'required': '确认密码不能为空',
            'max_length': '密码长度不能超过32个',
            'min_length': '密码长度不能少于6个',
        },
        label='确认密码',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        max_length=32,
        error_messages={
            'required': '用户名不能为空',
            'invalid': '请输入正确的邮箱格式',
        },
        label='邮箱',
        widget=widgets.EmailInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_user(self):
        user = self.cleaned_data.get('user')
        UserInfo.objects.filter(username=user).first()

        if not user:
            return user
        else:
            raise ValidationError('该用户已注册')

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')

        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致')
