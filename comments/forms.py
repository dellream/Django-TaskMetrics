from django import forms
from .models import Commentary


class EmailPostForm(forms.Form):
    """ Форма для отправки письма при нажатии 'Поделиться постом' """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentaryForm(forms.ModelForm):
    """ Форма для комментариев """
    class Meta:
        model = Commentary
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    """
    Форма для поиска
    """
    query = forms.CharField(label="Запрос")
