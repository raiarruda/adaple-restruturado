import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseRedirect, JsonResponse,
                         StreamingHttpResponse)
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render, render_to_response)
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .decorators import student_required, teacher_required
from .filters import EdpFilter
from .forms import Edp_form, form_recursos_edp, form_resposta_edp
from watson_developer_cloud import LanguageTranslatorV3
from .models import Edp, Habilidade, RecursosEdp, RespostaEdp

User = get_user_model()

@login_required
def edps(request):

    edps = Edp.objects.all()
    recursos = RecursosEdp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'

    user = request.user
    for x in user.respostaAluno.all():
        nivelx = x.edp.nivel
       
        print (nivelx == user.student.nivel )
    # edps_fala = 
    user.respostaAluno.filter()

    return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})

@teacher_required
def minhas_edps(request):
    edps = request.user.edps.all()
    recursos = RecursosEdp.objects.all()
    title = 'Estruturas Digitais Pedagogicas'
    template = 'edp/listarEDA.html'
    if request.user.eh_professor == True:
        return render(request, template, {'title': title, 'edps': edps, 'recursos': recursos})
    else:
        return redirect('edp:epds')

@student_required
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
    uploaded_file_url = 'media/none.mp4'


    if request.method == "POST":
        print("\nPOST\n")
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
            return HttpResponse(json.dumps({'url': reverse("edp:edps"), 'alerta': 'Recursos adicionados a EDA com sucesso'}), content_type='application/json')
        else:
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
        print("\nPOST\n")
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
            return HttpResponse(json.dumps({'url': reverse("edp:edps"), 'alerta':'Editado com sucesso!'}), content_type='application/json')
        else:
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
    uploaded_file_url = 'media/none.mp4'
    if request.method == "POST":
        print("\nPOST\n")
        form = form_resposta_edp(request.POST, request.FILES)

        if 'video' in request.FILES:
            myfile = request.FILES['video']
            #form = UploadFileForm(request.POST, request.FILES)
            fs = FileSystemStorage()
            filename = fs.save('video/' + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

        if form.is_valid():

            resposta = form.save(commit=False)
            resposta.video=uploaded_file_url
            resposta.edp = edp
            resposta.aprendiz = request.user
           
            resposta.save()
            return HttpResponse(json.dumps({'url': reverse("edp:edps"), 'alerta': 'Recursos adicionados a EDA com sucesso'}), content_type='application/json')
            
        else:
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

@teacher_required
def listarRespostasEDA(request):

    edpsTodas = Edp.objects.all()
    title = 'Estruturas Digitais Pedagogicas - Lista de EDA respondidas'
    template = 'edp/listarEDArespondida.html'
    edps = list()
   
   
    for edp in edpsTodas:
        
        if edp.respostas.all().count() != 0:
        
            edps.append(edp)
            
    print("\n--- Lista de respondidas \n ")
    return render(request, template, {'title': title, 'edps': edps})

def listaAlunosResponderamEdp(request, slug):
    edp = get_object_or_404(Edp, slug=slug)
    respostas = RespostaEdp.objects.filter(edp=edp).order_by('-aprendiz')
    lista_aprendiz=list()

    for r in range(len(respostas)):
        if r==0:
            lista_aprendiz.append(respostas[r])
        else:
            if respostas[r].aprendiz == respostas[r-1].aprendiz:
                pass
            else:
                lista_aprendiz.append(respostas[r])
    return render(request, 'edp/lista_alunos_EDARespondida.html', {'lista':lista_aprendiz})


def respostasEdp(request, id):
    resposta = get_object_or_404(RespostaEdp, id=id)
    edp = get_object_or_404(Edp, pk = resposta.edp.pk)
    aprendiz = get_object_or_404(User, pk = resposta.aprendiz.pk)
    respostas_edp = RespostaEdp.objects.filter(edp=edp, aprendiz=aprendiz)
    


    return render (request, 'edp/resposta.html', {'respostas':respostas_edp})

def traducao(request):
    template = 'edp/tradutor.html'
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        iam_apikey='k0JDRL55UH4gmh95MHKJI4ZBH78TBd2oAH7rKZMdIoB3',
        url='https://gateway.watsonplatform.net/language-translator/api'
    )


   
    if request.method == 'POST':
        origem = request.POST['origem']
        languages = language_translator.identify(origem).get_result()

        # languages = json.dumps(languages, indent=2)
  
        lingua_origem = languages['languages'][0]['language']

        # print(f'{lingua_origem}-pt')

        destino = language_translator.translate(text=origem,model_id=f'en-pt').get_result()

        return HttpResponse(json.dumps(destino), content_type='application/json')
        # //destino =tradutor.translate(origem, dest='pt').text
        return render(request, template, {'origem':origem, 'destino':destino})
    else:
        return render(request, template, {'origem':'', 'destino':''})

