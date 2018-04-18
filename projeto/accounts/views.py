# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def dashboard(request):
    title= 'Meu painel'
    template = 'dashboard.html'

    return render(request, template, {'title': title})
