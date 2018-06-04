from django import forms
from .models import Edp, Habilidade, Turma, Matricula, RecursosEdp, RespostaEdp, db_video
from django.db import transaction
from django.conf import settings
from django.utils.text import slugify


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
        fields = ('titulo', 'objetivo_pedagogico', 'atividades', 'metodologia', 'habilidades')
    
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
        fields = ('titulo','habilidades', 'objetivo_pedagogico', 'atividades', 'metodologia' )
    
    @transaction.atomic
    def save(self, request):
        
        edp = super().save(commit=False)
        edp.usuario = request.user
        
        edp.save()
        #edp = Edp.objects.create(usuario=edp.usuario)
        edp.habilidades.add(*self.cleaned_data.get('habilidades'))
        return edp



class form_recursos_edp(forms.ModelForm):
 
    video_embedded = forms.CharField(label='Video Externo',  required=True)
    texto = forms.CharField(label='Texto',  required=True, widget=forms.Textarea)


    class Meta:
        model = RecursosEdp

        fields = ('video_embedded', 'texto', 'recebe_texto', 'recebe_video_embedded', 'recebe_video', 'recebe_imagem')

class form_turma(forms.ModelForm):

    start_date = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Turma

        fields = ('nome', 'start_date',)
# class form_matricula(forms.ModelForm):
    # class Meta:
    #     model = Matricula

    #     fields= ('usuario', 'turma', 'status',)


class form_resposta_edp(forms.ModelForm):
 
    video_embedded = forms.CharField(label='Video Externo',  required=True)
    texto = forms.CharField(label='Texto',  required=True, widget=forms.Textarea)


    class Meta:
        model = RespostaEdp

        fields = ('video_embedded', 'texto')


class UploadFileForm(forms.ModelForm): 
   
    video_file = forms.FileField()
    class Meta:
        model = RecursosEdp
        fields = ['video', ]

