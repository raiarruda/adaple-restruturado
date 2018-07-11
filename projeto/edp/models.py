import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from tinymce.models import HTMLField

STATIC_CUR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

upload_storage = FileSystemStorage(location=STATIC_CUR_DIR)



User = get_user_model()

# Create your models here.
class Habilidade (models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Edp(models.Model):
    NIVEL_CHOICES = (
		(0, 'Básico (Sem certificação)'),
		(1, 'Intermediário'),
		(2, 'Intermediário Superior'),
        (3, 'Avançado'),
        (4, 'Avançado Superior')
	)

    titulo = models.CharField('Título', max_length=100)
    slug = models.SlugField('Atalho')
    objetivo_pedagogico = models.TextField('Objetivo Pegagogico')
    habilidades = models.ManyToManyField(Habilidade, related_name='habilidade_edp')    
    atividades = models.TextField('Atividades')
    metodologia = models.TextField('Metodologia')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='edps', on_delete=models.CASCADE)
    nivel = models.IntegerField('Nível de proficiência', choices=NIVEL_CHOICES, default=0,blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def iniciar(self):
        self.save()

    def __str__(self):
        return self.titulo
    
    @models.permalink
    def get_absolute_url(self):
        return ('edp:detalhe_edp', (), {'slug': self.slug})

    
    class Meta:
        verbose_name = 'Estrutura Digital de Aprendizagem'
        verbose_name_plural = 'Estruturas Digital de Aprendizagem'
        ordering = ['created_at']

class Turma(models.Model):
    nome = models.CharField('Nome', max_length=100)
	# Slug é um nome unico, sem espacos e em minusculas
    slug = models.SlugField('Atalho')
    start_date = models.DateField( 	'Data de Início', null=True, blank=True )
   # usuario = Fore
    # DateTimeField pega data e horario
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.nome

    #
    @models.permalink
    def get_absolute_url(self):
        return ('edp: turmas',(),{'slug':self.slug})
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['created_at']

class Matricula(models.Model):
    STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='matriculas', on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, verbose_name='Turma', related_name='matriculas', on_delete=models.CASCADE)
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1,blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def ativa_matricula(self):
        self.status = 1
        self.save()

    class Meta:
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'
        unique_together = (('usuario','turma'),)


class RecursosEdp(models.Model):
   
    edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='recursos', on_delete=models.CASCADE)
  #  edp = models.OneToOneField(Edp, verbose_name='Edp',  related_name='recursos', on_delete=models.CASCADE)
    video_embedded = EmbedVideoField(blank=True, null=True)
    texto =  models.TextField('Texto', blank=True)
    recebe_texto = models.BooleanField('Responder texto ?', default=False)
    recebe_video_embedded = models.BooleanField('Responder com videos do youtube?', default=False )
    recebe_video = models.BooleanField('Responder com video?', default=False)
    recebe_imagem = models.BooleanField('Responder com imagem ?', default=False)
    video = models.FileField(upload_to='media/videosenviados', storage=upload_storage, default="media/none.mp4")


    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.edp.titulo
    
    def iniciar(self):
        self.save()
 
    @models.permalink
    def get_absolute_url(self):
        return ('edp:detalhe_edp', (), {'slug': self.slug})

    
    class Meta:
        verbose_name = 'Recurso Estrutura Digital de Aprendizagem'
        verbose_name_plural = 'Recursos Estruturas  Digital de Aprendizagem'
        ordering = ['created_at']

        
class RespostaEdp(models.Model):
   
    edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='respostas', on_delete=models.CASCADE)
    video_embedded = EmbedVideoField(blank=True, null=True)
    texto = models.TextField('Texto', blank=True)
    video = models.FileField(upload_to='media/videosenviados', storage=upload_storage, default="media/none.mp4")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='respostas', on_delete=models.CASCADE)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def usuario(self):
        return self.edp.usuario
   
    def __str__(self):
        return self.edp.titulo
    
    def iniciar(self):
        self.save()

    class Meta:
        verbose_name = 'Resposta Estrutura Digital de Aprendizagem'
        verbose_name_plural = 'Resposta Estrutura Digital de Aprendizagem'
        ordering = ['edp']

class Video(models.Model):
    video = models.FileField(upload_to='media/videosenviados', storage=upload_storage, default="media/none.mp4")
    resposta = models.ForeignKey(RespostaEdp, verbose_name='Video_resposta', related_name='video_pk', on_delete=models.CASCADE)