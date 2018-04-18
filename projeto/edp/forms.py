from django import forms
from .models import Edp, Habilidade, Turma, Matricula, RecursosEdp



class form_edp(forms.ModelForm):

    titulo = forms.CharField(label='Título',  required=True)
    objetivo_pedagogico = forms.CharField(
        label='O que aprender? ',  required=True, widget=forms.Textarea)
    atividades = forms.CharField(label='O que fazer? ',  required=True, widget=forms.Textarea)
    metodologia = forms.CharField(label='Como fazer? ',  required=True, widget=forms.Textarea)

    class Meta:
        model = Edp

        fields = ('titulo', 'objetivo_pedagogico', 'atividades','metodologia',)

class form_recursos_edp(forms.ModelForm):
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