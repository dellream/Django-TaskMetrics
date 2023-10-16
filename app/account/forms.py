from django import forms
from django.contrib.auth.models import User

from .models import Profile


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


class UserEditForm(forms.ModelForm):
    """
    Форма изменения пользователя.
    """
    def clean_email(self):
        """
        Проверяет есть ли предоставляемый email в БД. Если есть, то райзит ошибку,
        иначе возвращает почту
        """
        email = self.cleaned_data['email']
        queryset = User.objects.filter(email=email).exclude(id=self.instance.id)
        if queryset.exists():
            raise forms.ValidationError('Эта электронная почта уже используется')
        return email

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }


class ProfileEditForm(forms.ModelForm):
    """
    Форма изменения профиля
    """
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения'
    )

    class Meta:
        model = Profile
        fields = [
            'birth_date',
            'avatar',
            'bio',
            'slug'
        ]
        labels = {
            'avatar': 'Фотография',
            'birth_date': 'Дата рождения',
            'bio': 'Информация о себе',
            'slug': 'Ссылка на профиль'
        }
