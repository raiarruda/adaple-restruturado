from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         StreamingHttpResponse)
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
# Create your views here.
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import (Edp_form,  UploadFileForm, form_edp,
                    form_recursos_edp, form_resposta_edp, form_turma, UploadFileFormResposta)
#from apiclient.discovery import build
from .models import Edp, Habilidade, Matricula, Turma, RecursosEdp

User = get_user_model()
#funcoes de listagem
@login_required
def edps(request):
    edps = Edp.objects.all()
    recursos = RecursosEdp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'
    

    return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})

@login_required
def minhas_edps(request):
    #edps = Edp.objects.filter(usuario=request.user)
    edps = request.user.edps.all()
    recursos = RecursosEdp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'
    

    return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})


@login_required
def turmas (request):
    turmas = Turma.objects.all()
    title = 'ADAPLE - TURMAS'
    template = 'edp/turmas.html'

    return render(request, template, {'title': title, 'turmas': turmas})

#funcoes de detalhes 
@login_required
def detalhe_edp(request, slug):
   
    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)
    form = form_resposta_edp()
    template = 'edp/edp_detalhes.html'
    title = edp.titulo + '- Detalhes'
    return render(request, template, {'title': title, 'edp': edp, 'recursos': recursos, 'form':form})

#funcoes de preecher formulario
#@login_required
def nova_edp(request):

    template = 'edp/edp_nova.html'
    title= 'Criar nova'
#    prof = request.User
    if request.method == "POST":
        form = Edp_form(request.POST)
        if form.is_valid():
            
            edp = form.save(request)
            #edp.usuario = settings.AUTH_USER_MODEL
            edp.slug = slugify(edp.titulo)
            #   edp.habilidades.add(cleaned_data.get('habilidades'))
            edp.save()

        edp.slug = slugify(edp.titulo)
        return redirect('edp:edps')

        # else:
        #     return redirect('edps:edps')
    else:
        form = Edp_form()
        return render( request, template, {'form':form})

# class nova_edp(CreateView):
#     model = Edp
#     form_class = Edp_form
#     template_name = 'edp/edp_nova.html'
#     #usuario = settings.AUTH_USER_MODEL
#     def get_context_data(self, **kwargs):
#        return super().get_context_data(**kwargs)

#     def form_valid(self, form):
        
#         edp = form.save()
       
#         return redirect('edp:edps')


@login_required
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
        return render( request, template, {'form':form, 'title':title})

@login_required
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
        return render( request, template, {'form':form, 'title':title, 'edp':edp})

#funcoes de clicar
@login_required
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


@login_required
def responder_edp(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)
    template = 'edp/responder_edp.html'
    title= 'Responder:- ' + edp.titulo
    
    if request.method == "POST":
            form = form_resposta_edp(request.POST)
            if form.is_valid():

                resposta_edp = form.save(commit=False)
                resposta_edp.edp=edp
                resposta_edp.save()

               # return redirect(reverse(edp.get_absolute_url()))
                return redirect('edp:edps')
            else:
                return redirect('edp:edps')
    else:
        form = form_resposta_edp()
        return render( request, template, {'form':form, 'title':title, 'edp':edp, 'recursos': recursos})


@csrf_exempt
def salvar_video(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
   
    if request.method == 'POST' and request.FILES['video_file']:
        myfile = request.FILES['video_file']
        form = UploadFileForm(request.POST, request.FILES)
        fs = FileSystemStorage()
        filename = fs.save('video/'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
       
        if form.is_valid():

            recursos_edp = form.save(commit=False)
            recursos_edp.edp=edp
            recursos_edp.video=uploaded_file_url
            recursos_edp.save()

        return render(request, 'edp/listarEDA.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'edp/camera.html')


@csrf_exempt
def salvar_video_resposta(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
   
    if request.method == 'POST' and request.FILES['video_file']:
        myfile = request.FILES['video_file']
        form = UploadFileFormResposta(request.POST, request.FILES)
        fs = FileSystemStorage()
        filename = fs.save('video/'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
       
        if form.is_valid():

            resposta_edp = form.save(commit=False)
            resposta_edp.edp=edp
            resposta_edp.video=uploaded_file_url
            resposta_edp.save()

        return render(request, 'edp/responder_edp.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'edp/camera.html')
