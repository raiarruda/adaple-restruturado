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
    path('detalhes/<slug:slug>', views.detalhe_edp, name= 'detalhe_edp'),
    path('nova/edp', views.nova_edp, name= "nova_edp"),
    path('editar/edp/<slug:slug>', views.editar_edp, name= "editar_edp"),
    path('deletar/edp/<slug:slug>', views.deletar_edp, name= "deletar_edp"),
    path('nova/turma', views.nova_turma, name= "nova_turma"),
    path('nova/matricula/<slug:slug>', views.nova_matricula, name= "nova_matricula"),
    path('adicionar/recursos/<slug:slug>', views.adicionar_recursos, name= "adicionar_recursos"),
    path('responder/<slug:slug>', views.responder_edp, name="responder_edp"),
    path('turmas', views.turmas, name= "turmas"),
    path('camera/<slug:slug>', views.salvar_video, name="camera"),
    path('pesquisa', views.pesquisaEdp, name='pesquisa'),
    path('pesquisa2', FilterView.as_view(filterset_class=EdpFilter, template_name='edp/pesquisa.html'), name='pesquisa2'),
    path('camera2/<slug:slug>', views.salvar_video_resposta, name="camera_resposta"),
]