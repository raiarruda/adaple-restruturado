# accounts/urls.py
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
app_name='edp'

urlpatterns = [
    path('', views.edps, name='edps'),
    path('minhas', views.minhas_edps, name='minhas_edps'),
    path('detalhes/<slug:slug>', views.detalhe_edp, name= 'detalhe_edp'),
    path('nova/edp', views.nova_edp, name= "nova_edp"),
    path('nova/turma', views.nova_turma, name= "nova_turma"),
    path('nova/matricula/<slug:slug>', views.nova_matricula, name= "nova_matricula"),
    path('adicionar/recursos/<slug:slug>', views.adicionar_recursos, name= "adicionar_recursos"),
    path('responder/<slug:slug>', views.responder_edp, name="responder_edp"),
    path('turmas', views.turmas, name= "turmas"),
    path('camera/<slug:slug>', views.salvar_video, name="camera"),
    path('camera2/<slug:slug>', views.salvar_video_resposta, name="camera_resposta"),
  #  path('login/', auth_views.LoginView.as_view(), name='login'),
]