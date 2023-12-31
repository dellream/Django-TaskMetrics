from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from education.models import Course


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль'
    )


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

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Этот псевдоним уже используется.')
        return data


class UserUpdateForm(forms.ModelForm):
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


class ProfileUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения',
        help_text='Введите вашу дату рождения'
    )

    delete_avatar = forms.BooleanField(
        required=False,
        initial=False,
        label='Удалить текущую фотографию',
        help_text='Отметьте, если хотите удалить текущую фотографию'
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
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CourseEnrollForm(forms.Form):
    """
    Форма для зачисления студентов на курсы
    """
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.HiddenInput
    )
