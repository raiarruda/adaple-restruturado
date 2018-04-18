from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.text import slugify
from .models import Edp, Habilidade, Turma, Matricula
from .forms import form_edp, form_turma, form_recursos_edp
from django.contrib import messages
# Create your views here.
from django.urls import reverse

#funcoes de listagem

def edps(request):
    edps = Edp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/edps.html'

    return render(request, template, {'title': title, 'edps': edps})


def turmas (request):
    turmas = Turma.objects.all()
    title = 'ADAPLE - TURMAS'
    template = 'edp/turmas.html'

    return render(request, template, {'title': title, 'turmas': turmas})

#funcoes de detalhes 

def detalhe_edp(request, slug):
   
    edp = get_object_or_404(Edp, slug=slug)
    template = 'edp/edp_detalhes.html'
    title = edp.titulo + '- Detalhes'

    return render(request, template, {'title': title, 'edp': edp})

#funcoes de preecher formulario

def nova_edp(request):
    # TODO: habilidades
    template = 'edp/edp_nova.html'
    title= 'Criar nova'

    if request.method == "POST":
            form = form_edp(request.POST)
            if form.is_valid():

                edp = form.save(commit=False)
                edp.usuario = request.user
                edp.slug = slugify(edp.titulo)
                edp.save()

                return redirect('edp:edps')
            else:
                return redirect('edps:edps')
    else:
        form = form_edp()
        return render( request, template, {'form':form})


def nova_turma(request):
    template = 'edp/turma_nova.html'
    title= 'Criar nova turma'

    if request.method == "POST":
            form = form_turma(request.POST)
            if form.is_valid():

                turma = form.save(commit=False)
                turma.slug = slugify(turma.nome)
                turma.save()
                messages.success(request, 'Turma criada')

                return redirect('edp:turmas')
            else:
                messages.info(request, 'turma não criada')
                return redirect('edp:edps')
    else:
        form = form_turma()
        return render( request, template, {'form':form})


def adicionar_recursos(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    template = 'edp/adicionar_recursos.html'
    title= 'Adicionar Recursos a EDP - ' + edp.titulo
    
    if request.method == "POST":
            form = form_recursos_edp(request.POST)
            if form.is_valid():

                recursos_edp = form.save(commit=False)
                recursos_edp.edp=edp
                recursos_edp.save()

               # return redirect(reverse(edp.get_absolute_url()))
                return redirect('edp:edps')
            else:
                return redirect('edp:edps')
    else:
        form = form_recursos_edp()
        return render( request, template, {'form':form})

#funcoes de clicar

def nova_matricula(resquest, slug):
    
    turma = get_object_or_404(Turma, slug=slug)
    # Metodo get_or_create se passa um filtro para ele, no caso o usuario atual, e o curso
    matricula, created = Matricula.objects.get_or_create(usuario=resquest.user, turma=turma)
    if created:
        #enrollment.active()
        messages.success(resquest, 'Você foi inscrito no curso com sucesso.')
    else:
        messages.info(resquest, 'Você já está inscrito no curso.')
    return redirect('accounts:dashboard')

