from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import fields, widgets

from index.models import users


class EnrollForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
                               error_messages={'required':'用户名不能为空'})
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '昵称'}),
                               error_messages={'required':'昵称不能为空'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'密码'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'重复密码'}))

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise ValidationError('密码不一致！')
        else:
            return self.cleaned_data