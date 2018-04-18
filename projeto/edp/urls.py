# accounts/urls.py
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
app_name='edp'

urlpatterns = [
    path('', views.lista_edps, name='edps'),
    path('detalhes/<slug:slug>', views.detalhe_edp, name= 'detalhe_edp'),
    path('nova', views.nova_edp, name= "nova_edp"),
  #  path('login/', auth_views.LoginView.as_view(), name='login'),
]