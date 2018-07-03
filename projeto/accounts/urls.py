# accounts/urls.py
from django.urls import path

from django.contrib.auth import views as auth_views

from django.contrib.auth import get_user_model
User = get_user_model()
from projeto.accounts import views
app_name='accounts'

urlpatterns = [
 #não existe mais mas não tenho coragem de deletar ainda   path('signup/', views.SignUp.as_view(), name='signup'), 
    path('', auth_views.LoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'), 
    path('cadastro/aluno/', views.CadastroAlunoView.as_view(), name='cadastro_aluno'),
    path('cadastro/professor/', views.CadastroProfessorView.as_view(), name='cadastro_professor'),

]