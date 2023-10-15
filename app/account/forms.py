from django import forms
from django.contrib.auth.models import User


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Ваш псевдоним (включая только буквы, цифры и @/./+/-/_):'
    )
    first_name = forms.CharField(label='Ваше имя')
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Эта электронная почта уже используется.')
        return data
