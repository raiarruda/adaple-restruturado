from django import forms

from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'O que você pensa?',}
        ),
        label="Mensagem",
        max_length=4000,
        help_text='Tamanho máximo 4000 caracteres.'
    )
    subject=forms.CharField(max_length=150, label="Assunto")

    class Meta:
        model = Topic
        fields = ['subject', 'message']