from django import forms

from .models import Topic, Board

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

class NewBoardForm(forms.ModelForm):
    name = forms.CharField(label="Nome",
        max_length=30
    )
    description=forms.CharField(max_length=100, label="Descrição")

    class Meta:
        model = Board
        fields = ['name', 'description']

