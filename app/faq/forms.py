from django import forms
from .models import Commentary


class CommentaryForm(forms.ModelForm):
    """ Форма для комментариев """

    class Meta:
        model = Commentary
        fields = ['name', 'email', 'body']
