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
from django.http import Http404
from .filters import EdpFilter
from .forms import (Edp_form, UploadFileForm, UploadFileFormResposta,
                    form_recursos_edp, form_resposta_edp, form_turma, video_form_resposta)
from .models import Edp, Habilidade, Matricula, RecursosEdp, Turma, RespostaEdp
from .decorators import student_required, teacher_required
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
    if request.user.eh_professor==True:
        return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})
    else:
        return redirect('edp:epds')

@login_required
def minhas_edps_aluno(request):
    edps = request.user.edps.all()
    recursos = RecursosEdp.objects.all()
   
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'
    if request.user.eh_aluno==True:
        return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})
    else:
        return redirect('edp:epds')

@login_required
def turmas (request):
    turmas = Turma.objects.all()
    title = 'ADAPLE - TURMAS'
    template = 'edp/turmas.html'

    return render(request, template, {'title': title, 'turmas': turmas})

#funcoes de detalhes 
# @login_required
@teacher_required
def detalhe_edp(request, slug):
   
    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)
    form = form_resposta_edp()
    template = 'edp/edp_detalhes.html'
    title = edp.titulo + '- Detalhes'
    return render(request, template, {'title': title, 'edp': edp, 'recursos': recursos, 'form':form})

#funcoes de preecher formulario
@login_required
def nova_edp(request):
    template = 'edp/edp_nova.html'
    title= 'Criar nova'
    if request.method == "POST":
        form = Edp_form(request.POST)
        if form.is_valid():
            
            edp = form.save(request)

            edp.slug = slugify(edp.titulo)+"-"+str(edp.pk)
            edp.save()
    
        return redirect('edp:edps')
    else:
        form = Edp_form()
        return render( request, template, {'form':form})

@login_required
def editar_edp(request,slug):
    edp =  get_object_or_404(Edp, slug=slug)
   
    template = 'edp/edp_nova.html'
    title= 'Editar EDA' + edp.titulo
    if request.method == 'POST':
        form = Edp_form(request.POST, instance=edp)
        if form.is_valid():
            form.save(request)
            return redirect('edp:edps')
    else:
        form = Edp_form(instance=edp)
    return render( request, template, {'form':form})


@login_required
def deletar_edp(request, slug):
    template = 'edp/edp_deletar.html'
    edp = get_object_or_404(Edp, slug=slug)
    if request.method == 'POST':
        edp.delete()
        return redirect('edp:edps')
    return render(request, template, {'edp':edp})

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
    title= 'Adicionar Recursos a EDA - ' + edp.titulo
    
    if request.method == "POST":
            form = form_recursos_edp(request.POST)
            if form.is_valid():

                recursos_edp = form.save(commit=False)
                recursos_edp.edp=edp
                recursos_edp.save()

                return redirect('edp:edps')
               # return render( request, template, {'form':form, 'title':title, 'edp':edp})
            else:
                return redirect('edp:edps')
    else:
        form = form_recursos_edp()
        return render( request, template, {'form':form, 'title':title, 'edp':edp})


@login_required
def editar_recursos(request,slug):
    edp =  get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404(RecursosEdp, edp=edp)

    template = 'edp/adicionar_recursos.html'
    title= 'Editar Recursos da EDA' + edp.titulo
    if request.method == 'POST':
        form = form_recursos_edp(request.POST, instance=recursos)
        if form.is_valid():
            form.save(request)
            return tredirect('edp:edps')
    else:
        form = form_recursos_edp(instance=recursos)
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
    template = 'edp/edp_responder.html'
    title= 'Responder EDA: ' + edp.titulo
    

    if request.method == 'POST' and request.FILES['video_file']:
        print ("entrou no files")
        myfile = request.FILES['video_file']
        form = UploadFileForm(request.POST, request.FILES)
        fs = FileSystemStorage()
        filename = fs.save('video/'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if form.is_valid():
            resposta_edp = form.save(commit=False)
            resposta_edp.edp = epd
            resposta_edp.video = uploaded_file_url
            resposta_edp.save()
        return render(request, 'edp/responder_edp.html', {
            'uploaded_file_url': uploaded_file_url
        })


    elif request.method == "POST":
        print ("\n \n\ \n\ \nnãoooooo entrou no files")
        form = form_resposta_edp(request.POST)
        if form.is_valid():

            resposta_edp = form.save(commit=False)
            resposta_edp.edp=edp
            resposta_edp.save()

            #return redirect(reverse(edp.get_absolute_url()))
        return redirect('edp:edps')

    
    else:
        form = form_resposta_edp()
        return render( request, template, {'form':form, 'title':title, 'edp':edp, 'recursos': recursos})



@login_required
# def salvar_video_resposta(request, pk):
#      resposta = get_object_or_404(Edp, slug=slug)
#     if request.method == 'POST' and request.FILES['video_file']:
#         myfile = request.FILES['video_file']
#         form = UploadFileFormResposta(request.POST, request.FILES)
#         fs = FileSystemStorage()
#         filename = fs.save('video/'+ myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
       
#         if form.is_valid():

#             resposta_edp.video=uploaded_file_url
#             resposta_edp.save()

#         return render(request, 'edp/responder_edp.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, template_name)





@csrf_exempt
def salvar_video(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    recursos =  get_object_or_404(RecursosEdp, edp=edp)
    if request.method == 'POST' and request.FILES['video_file']:
        myfile = request.FILES['video_file']
        form = UploadFileForm(request.POST, request.FILES)
        fs = FileSystemStorage()
        filename = fs.save('video/'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
       
        if form.is_valid():

          #  recursos_edp = form.save(commit=False)
           # recursos_edp.edp=edp
         #   recursos_edp.video=uploaded_file_url
          
            recursos.video= uploaded_file_url
            #recursos_edp.save()

        return render(request, 'edp/listarEDA.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'edp/camera.html')

def editar_video(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    recursos = get_object_or_404( RecursosEdp, edp=edp)

    if request.method == 'POST' and request.FILES['video_file']:
        myfile = request.FILES['video_file']
        form = UploadFileForm(request.POST, request.FILES)
        fs = FileSystemStorage()
        filename = fs.save('video/'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
       
        if form.is_valid():
            recursos.video=uploaded_file_url
            form.save(request)
            return redirect('edp:edps')

        return render(request, 'edp/listarEDA.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'edp/camera.html')



@login_required
def pesquisaEdp(request):
    template_name = 'edp/pesquisa.html'
    title = "Pesquisa"
    edps = Edp.objects.all()
    edps_pesquisa = EdpFilter(request.GET, queryset=edps)

    return render(request, template_name, {'edps_pesquisa': edps_pesquisa, 'title': title})
