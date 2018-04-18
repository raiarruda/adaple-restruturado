from django.shortcuts import render, redirect, render_to_response
from django.http import HttpRequest, HttpResponse
from django.utils.text import slugify
from .models import Edp, Habilidade
from .forms import form_edp
# Create your views here.


def lista_edps(request):
    edps = Edp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/edps.html'

    return render(request, template, {'title': title, 'edps': edps})


def detalhe_edp(request, slug):
    assert isinstance(request, HttpRequest)

    edp = Edp.objects.all().get(slug=slug)
    template = 'edp/edp_details.html'
    title = edp.titulo + '- Detalhes'

    return render(request, template, {'title': title, 'edp': edp})


def nova_edp(request):
    # TODO: habilidades
    template = 'edp/edp_criar.html'
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


