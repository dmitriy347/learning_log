from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        # Форма создается на базе модели Topic.
        model = Topic
        # На ней размещается только поле 'text'.
        fields = ['text']
        # Приказывает Django не генерировать подпись для текстового поля.
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}