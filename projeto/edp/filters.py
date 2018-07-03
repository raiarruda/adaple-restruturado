from projeto.edp.models import Edp, RecursosEdp, RespostaEdp, Habilidade
from django import forms
from django.contrib.auth import get_user_model

import django_filters
User = get_user_model()


class EdpFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr=['contains'])
    habilidades = django_filters.ModelMultipleChoiceFilter(queryset= Habilidade.objects.all(),  widget=forms.CheckboxSelectMultiple)
    usuario = django_filters.ModelChoiceFilter(queryset=User.objects.filter(eh_professor=True))
    class Meta:
        model = Edp
        fields = ['nivel', 'habilidades', 'usuario']