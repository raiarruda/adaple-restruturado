# accounts/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, TemplateView

from projeto.accounts.forms import CadastroAlunoForm, CadastroProfessorForm
from projeto.accounts.models import Student, User
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class CadastroAlunoView(CreateView):
    model = User
    form_class = CadastroAlunoForm
    template_name = 'registration/cadastroForm.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'aluno'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:dashboard')

class CadastroProfessorView(CreateView):
    model = User
    form_class = CadastroProfessorForm
    template_name = 'registration/cadastroForm.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'professor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:dashboard')


class CadastroView(TemplateView):
    template_name = 'registration/cadastro.html'


def dashboard(request):
    title= 'Meu painel'
    template = 'dashboard.html'
    usuario = request.user

    if usuario.eh_professor:
        return redirect('edp:edps')
    else:
        return render(request, template, {'title': title})
