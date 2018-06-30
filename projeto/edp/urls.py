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
    path('respondidas', views.minhas_edps_aluno, name='respondidas'),
    path('detalhes/<slug:slug>', views.detalhe_edp, name= 'detalhe_edp'),
    
    path('nova/edp', views.nova_edp, name= "nova_edp"),
    path('adicionar/recursos/<slug:slug>', views.adicionar_recursos, name= "adicionar_recursos"),
    path('nova/matricula/<slug:slug>', views.nova_matricula, name= "nova_matricula"),
    path('nova/turma', views.nova_turma, name= "nova_turma"),

    path('editar/edp/<slug:slug>', views.editar_edp, name= "editar_edp"),
    path('editar/edp/recursos/<slug:slug>', views.editar_recursos, name='editar_recursos'),
    
    path('deletar/edp/<slug:slug>', views.deletar_edp, name= "deletar_edp"),
#TODO    path('deletar/edp/<slug:slug>', views.deletar_edp, name= "deletar_edp"),  
    
    path('responder/<slug:slug>', views.responder_edp, name="responder_edp"),
    path('turmas', views.turmas, name= "turmas"),
    
    path('pesquisa', views.pesquisaEdp, name='pesquisa'),

    path('camera/<slug:slug>', views.salvar_video, name="camera"),
    path('camera_ed/<slug:slug>', views.editar_video, name="ed_camera"),
    # path('camera2/<slug:slug>', views.salvar_video_resposta, name="camera_resposta"),
]