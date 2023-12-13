from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation

from catalog.models import AdvUser, Application, Category
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    LetterValidator = RegexValidator(r'^[- а-яА-Я]*$')
    LoginValidator = RegexValidator(r'^[- a-zA-Z]*$')
    username = forms.CharField(validators=[LoginValidator], required=True, label='Логин',
                               help_text='Только латиница и дефис, уникальный')
    fullname = forms.CharField(validators=[LetterValidator], required=True, label='ФИО',
                               help_text='Только кириллические буквы, дефис и пробелы')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    consent = forms.BooleanField(widget=forms.CheckboxInput, required=True,
                                 label='Согласие на обработку персональных данных')

    class Meta:
        model = AdvUser
        fields = ('username', 'fullname', 'email', 'password', 'password2', 'consent')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_password1(self):
        password = self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)
        return password


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'summary', 'category', 'image']


class ApplicationDesignForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['design']


class ApplicationCommentForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['comment']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
