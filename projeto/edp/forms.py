from django import forms
from .models import Edp, Habilidade



class form_edp(forms.ModelForm):

    titulo = forms.CharField(label='Título',  required=True)
    objetivo_pedagogico = forms.CharField(
        label='O que aprender? ',  required=True, widget=forms.Textarea)
    atividades = forms.CharField(label='O que fazer? ',  required=True, widget=forms.Textarea)
    metodologia = forms.CharField(label='Como fazer? ',  required=True, widget=forms.Textarea)

    class Meta:
        model = Edp

        fields = ('titulo', 'objetivo_pedagogico', 'atividades','metodologia',)

