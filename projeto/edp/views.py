import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import (Http404, HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse)
from django.shortcuts import (get_object_or_404, redirect, render, render_to_response)
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from .decorators import student_required, teacher_required
from .filters import EdpFilter
from .forms import Edp_form, form_recursos_edp, form_resposta_edp
from .models import Edp, Habilidade, RecursosEdp, RespostaEdp

User = get_user_model()


@login_required
def edps(request):

    edps = Edp.objects.all()
    recursos = RecursosEdp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'

    return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})


@login_required
def minhas_edps(request):
    edps = request.user.edps.all()
    recursos = RecursosEdp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'
    if request.user.eh_professor == True:
        return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})
    else:
        return redirect('edp:epds')


@login_required
def minhas_edps_aluno(request):
    edps = request.user.edps.all()
    recursos = RecursosEdp.objects.all()

    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'
    if request.user.eh_aluno == True:
        return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})
    else:
        return redirect('edp:epds')


@teacher_required
def detalhe_edp(request, slug):

    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)
    form = form_resposta_edp()
    template = 'edp/edp_detalhes.html'
    title = edp.titulo + '- Detalhes'
    return render(request, template, {'title': title, 'edp': edp, 'recursos': recursos, 'form': form})


@teacher_required
def nova_edp(request):
    template = 'edp/edp_nova.html'
    title = 'Criar nova'
    if request.method == "POST":
        form = Edp_form(request.POST)
        if form.is_valid():

            edp = form.save(request)

            edp.slug = slugify(edp.titulo)+"-"+str(edp.pk)
            edp.save()

        return redirect('edp:edps')
    else:
        form = Edp_form()
        return render(request, template, {'form': form})


@teacher_required
def editar_edp(request, slug):
    edp = get_object_or_404(Edp, slug=slug)

    template = 'edp/edp_nova.html'
    title = 'Editar EDA' + edp.titulo
    if request.method == 'POST':
        form = Edp_form(request.POST, instance=edp)
        if form.is_valid():
            form.save(request)
            return redirect('edp:edps')
    else:
        form = Edp_form(instance=edp)
    return render(request, template, {'form': form})


@teacher_required
def deletar_edp(request, slug):
    template = 'edp/edp_deletar.html'
    edp = get_object_or_404(Edp, slug=slug)
    if request.method == 'POST':
        edp.delete()
        return redirect('edp:edps')
    return render(request, template, {'edp': edp})



@teacher_required
def adicionar_recursos(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    template = 'edp/adicionar_recursos.html'
    title = 'Adicionar Recursos a EDA - ' + edp.titulo

    if request.method == "POST":
        print("aqui")
        form = form_recursos_edp(request.POST, request.FILES)

        if 'video' in request.FILES:
            myfile = request.FILES['video']
            #form = UploadFileForm(request.POST, request.FILES)
            fs = FileSystemStorage()
            filename = fs.save('video/' + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

        if form.is_valid():

            recursos_edp = form.save(commit=False)
            recursos_edp.edp = edp
            recursos_edp.video=uploaded_file_url
            recursos_edp.save()
            print("aui2")
            return Response(json.dumps({'url': reverse("../edps/")}), content_type='application/json')
            # return reverse('edp:edps')
           # return render( request, template, {'form':form, 'title':title, 'edp':edp})
        else:
            print("aqui3")
            print(form.errors.as_json)
            return redirect('edp:edps')
    else:
        form = form_recursos_edp()
        return render(request, template, {'form': form, 'title': title, 'edp': edp})

@teacher_required
def editar_recursos(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)
    template = 'edp/adicionar_recursos.html'
    title = 'Editar Recursos da EDA - ' + edp.titulo
    uploaded_file_url = recursos.video

    if request.method == "POST":
        print("aqui")
        form = form_recursos_edp(request.POST, request.FILES, instance=recursos)

        if 'video' in request.FILES:
            myfile = request.FILES['video']
            # form = UploadFileForm(request.POST, request.FILES)
            fs = FileSystemStorage()
            filename = fs.save('video/' + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

        if form.is_valid():
            form.video=uploaded_file_url
            form.save(request)
            return Response(json.dumps({'url': reverse("../edps/")}), content_type='application/json')
            # return reverse('edp:edps')
           # return render( request, template, {'form':form, 'title':title, 'edp':edp})
        else:
            print("aqui3")
            print(form.errors.as_json)
            return redirect('edp:edps')
    else:
        form = form_recursos_edp(instance=recursos)
        return render(request, template, {'form': form, 'title': title, 'edp': edp})

@teacher_required
def editar_edp(request, slug):
    edp = get_object_or_404(Edp, slug=slug)

    template = 'edp/edp_nova.html'
    title = 'Editar EDA' + edp.titulo
    if request.method == 'POST':
        form = Edp_form(request.POST, instance=edp)
        if form.is_valid():
            form.save(request)
            return redirect('edp:edps')
    else:
        form = Edp_form(instance=edp)
    return render(request, template, {'form': form})

@student_required
def responder_edp(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)
    template = 'edp/edp_responder.html'
    title = 'Responder a EDA - ' + edp.titulo
    # uploaded_file_url = 'media/none.mp4'
    if request.method == "POST":
        print("aqui")
        form = form_resposta_edp(request.POST, request.FILES)

        if 'video' in request.FILES:
            myfile = request.FILES['video']
            #form = UploadFileForm(request.POST, request.FILES)
            fs = FileSystemStorage()
            filename = fs.save('video/' + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            resposta.video=uploaded_file_url

        if form.is_valid():

            resposta = form.save(commit=False)
            resposta.edp = edp
            resposta.usuario = request.user
           
            resposta.save()
            print("aui2")
            # return Response(json.dumps({'url': reverse("../edps/")}), content_type='application/json')
            return reverse('edp:edps')
           # return render( request, template, {'form':form, 'title':title, 'edp':edp})
        else:
            print("aqui3")
            print(form.errors.as_json)
            return redirect('edp:edps')
    else:
        form = form_resposta_edp()
        return render(request, template, {'form': form, 'title': title, 'edp': edp, 'recursos': recursos})


@login_required
def pesquisaEdp(request):
    template_name = 'edp/pesquisa.html'
    title = "Pesquisa"
    edps = Edp.objects.all()
    edps_pesquisa = EdpFilter(request.GET, queryset=edps)

    return render(request, template_name, {'edps_pesquisa': edps_pesquisa, 'title': title})
