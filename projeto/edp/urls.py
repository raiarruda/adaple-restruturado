# accounts/urls.py
from django.urls import path
from django_filters.views import FilterView
from django.contrib.auth import views as auth_views
from projeto.edp.filters import EdpFilter
from . import views
app_name='edp'

urlpatterns = [
    path('', views.edps, name='edps'),
    path('minhas', views.minhas_edps, name='minhas_edps'),
    path('edp/respondidas', views.listarRespostasEDA, name='respondidas'),

    path('aluno/<int:id>/respostas', views.respostasEdp, name='resposta_edp'),

    path('edp/<slug:slug>/alunos', views.listaAlunosResponderamEdp, name='responderam'),
    path('edp/detalhes/<slug:slug>', views.detalhe_edp, name= 'detalhe_edp'),
    path('edp/nova', views.nova_edp, name= "nova_edp"),
    path('edp/adicionar/recursos/<slug:slug>', views.adicionar_recursos, name= "adicionar_recursos"),
    path('edp/editar/<slug:slug>', views.editar_edp, name= "editar_edp"),
    path('edp/recursos/editar/<slug:slug>', views.editar_recursos, name='editar_recursos'),
    path('edp/deletar/<slug:slug>', views.deletar_edp, name= "deletar_edp"),
    path('edp/responder/<slug:slug>', views.responder_edp, name="responder_edp"),
    path('edp/pesquisa', views.pesquisaEdp, name='pesquisa'),

]