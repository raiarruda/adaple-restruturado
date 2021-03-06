from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf import settings
from django.db import transaction
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField

from .models import Edp, Habilidade, RecursosEdp, RespostaEdp


class Edp_form(forms.ModelForm):

    titulo = forms.CharField(
        label='Título',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "Digite aqui o nome de sua EDA"}))
    objetivo_pedagogico = forms.CharField(
        label='O que aprender? (Objetivo) ',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': "Digite aqui, com poucas palavras, o objetivo de aprendizagem principal."}))
    atividades = forms.CharField(
        label='O que fazer? (Atividades)',
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': "Digite aqui as atividades que serão necessárias para usar a EDA."}))
    metodologia = forms.CharField(
        label='Como fazer? (Método) ',
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': "Digite aqui como as atividades deverão ser realizadas e quais recursos deverão ser utilizados para usar a EDA."}))
    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta():
        model = Edp
        fields = ('titulo', 'habilidades', 'nivel',
                  'objetivo_pedagogico', 'atividades', 'metodologia')

    @transaction.atomic
    def save(self, request):

        edp = super().save(commit=False)
        edp.usuario = request.user

        edp.save()
        edp.habilidades.add(*self.cleaned_data.get('habilidades'))
        return edp


class form_recursos_edp(forms.ModelForm):

    video_embedded = forms.CharField(label='Vídeo Externo',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': "Cole aqui um link de um video do youtube ou vimeo"}
        )
        )
    texto = forms.CharField(
        label='Texto',
        widget=forms.Textarea(
            attrs={'placeholder': "Digite aqui um exemplo ou um texto: poesia, música, carta, etc."}),
        required=False)

    recebe_texto = forms.BooleanField(
        label='O aprendiz deve digitar um texto.',
        widget=forms.CheckboxInput,
        required=False
    )
    recebe_video_embedded = forms.BooleanField(
        label='O aprendiz deve inserir um vídeo do Youtube ou Vimeo.',
        widget=forms.CheckboxInput,
        required=False
    )
    recebe_video = forms.BooleanField(
        label='O aprendiz deve gravar um vídeo.',
        widget=forms.CheckboxInput,
        required=False
    )
    video = forms.FileField(
              required=False
    )

    class Meta:
        model = RecursosEdp
        fields = ('video_embedded', 'video', 'texto', 'recebe_texto',
                  'recebe_video_embedded', 'recebe_video', 'recebe_imagem')


class form_resposta_edp(forms.ModelForm):
    video_embedded = forms.CharField(label='Vídeo Externo',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': "Cole aqui um link de um video do youtube ou vimeo"})
        )
    texto = forms.CharField(
        label='Texto',   
        widget=forms.Textarea (
            attrs={'placeholder':"Digite aqui a sua resposta."}), 
        required=False
        )
    video = forms.FileField(required=False)

    class Meta:
        model = RespostaEdp
        fields = ('video_embedded', 'texto', 'video')
    # @transaction.atomic
    # def save(self, request):

    #     resposta = super().save(commit=False)
    #     edp.aprendiz = request.user

    #     res.save()
    #     edp.habilidades.add(*self.cleaned_data.get('habilidades'))
    #     return edp