from django import forms
from .models import Commentary


class CommentaryForm(forms.ModelForm):
    """ Форма для комментариев """

    class Meta:
        model = Commentary
        fields = ['body']

    def __init__(self, *args, **kwargs):
        # Передаем request в форму, чтобы использовать его в clean() или в save()
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Создаем объект класса Commentary, не сохраняя его в базе данных
        commentary = super().save(commit=False)

        # Если request был передан, используем текущего пользователя в качестве автора
        if self.request:
            commentary.author = self.request.user

        # Сохраняем комментарий в базе данных
        if commit:
            commentary.save()

        return commentary
