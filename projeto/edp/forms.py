from django import forms
from .models import Edp, Habilidade, Turma, Matricula, RecursosEdp, RespostaEdp, Video
from django.db import transaction
from django.conf import settings
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField
from ckeditor.widgets import CKEditorWidget
class form_edp(forms.ModelForm):

    titulo = forms.CharField(label='Título',  required=True)
    objetivo_pedagogico = forms.CharField(
        label='O que aprender? ',  required=True, widget=forms.Textarea)
    atividades = forms.CharField(label='O que fazer? ',  required=True, widget=forms.Textarea)
    metodologia = forms.CharField(label='Como fazer? ',  required=True, widget=forms.Textarea)
    habilidades = forms.ModelMultipleChoiceField(
            label='Quais habilidades trabalhas??',
            queryset= Habilidade.objects.all(),
            widget= forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Edp
        fields = ('titulo', 'objetivo_pedagogico','nivel', 'atividades', 'metodologia', 'habilidades')
    
  #  @transaction.atomic
   # def save(self)
    #    user= super().save(commit=False)
     #   user.save()

class Edp_form(forms.ModelForm):
    
    titulo = forms.CharField(label='Título',  required=True)
    objetivo_pedagogico = forms.CharField(
        label='O que aprender? ',  required=True, widget=forms.Textarea)
    atividades = forms.CharField(label='O que fazer? ',  required=True, widget=forms.Textarea)
    metodologia = forms.CharField(label='Como fazer? ',  required=True, widget=forms.Textarea)
    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta():
        model = Edp
        fields = ('titulo','habilidades', 'nivel', 'objetivo_pedagogico', 'atividades', 'metodologia' )
    
    @transaction.atomic
    def save(self, request):
        
        edp = super().save(commit=False)
        edp.usuario = request.user
        
        edp.save()
        #edp = Edp.objects.create(usuario=edp.usuario)
        edp.habilidades.add(*self.cleaned_data.get('habilidades'))
        return edp



class form_recursos_edp(forms.ModelForm):
 
    video_embedded = forms.CharField(label='Video Externo', required=False)
    texto = forms.CharField(label='Texto',   widget=forms.Textarea, required=False)

    class Meta:
        model = RecursosEdp

        fields = ('video_embedded', 'texto', 'recebe_texto', 'recebe_video_embedded', 'recebe_video', 'recebe_imagem')



class form_resposta_edp(forms.ModelForm):
 
    video_embedded = forms.CharField(label='Video Externo', required=False)
    texto = forms.CharField(label='Texto', widget=forms.Textarea, required=False)

    class Meta:
        model = RespostaEdp

        fields = ('video_embedded', 'texto')
        
    # @transaction.atomic
    # def save(self):
    #     resposta = super().save(commit=False)
    #     resposta.usuario = request.user
    #     resposta.save()
    #     video = Video.objects.create(resposta=resposta)
    #     return resposta

class UploadFileForm(forms.ModelForm): 
   
    video_file = forms.FileField()
    class Meta:
        model = RecursosEdp
        fields = ['video', ]

class UploadFileFormResposta(forms.ModelForm): 
   
    video_file = forms.FileField()
    class Meta:
        model = RecursosEdp
        fields = ['video', ]


class video_form_resposta(forms.ModelForm):
    video = forms.FileField()

    class Meta:
        model = Video
        fields = ['video',]

class form_turma(forms.ModelForm):

    start_date = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Turma

        fields = ('nome', 'start_date',)

