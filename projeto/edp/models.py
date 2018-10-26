import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from tinymce.models import HTMLField
from projeto.accounts.models import Student
STATIC_CUR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

upload_storage = FileSystemStorage(location=STATIC_CUR_DIR)



User = get_user_model()

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
        ordering = ['-created_at']

class RecursosEdp(models.Model):
   
    # edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='recursos', on_delete=models.CASCADE)
    edp = models.OneToOneField(Edp, verbose_name='Edp',  related_name='recursos', on_delete=models.CASCADE)
    video_embedded = EmbedVideoField(blank=True, null=True)
    texto =  models.TextField('Texto', blank=True)
    recebe_texto = models.BooleanField('Responder texto ?', default=False)
    recebe_video_embedded = models.BooleanField('Responder com videos do youtube?', default=False )
    recebe_video = models.BooleanField('Responder com video?', default=False)
    recebe_imagem = models.BooleanField('Responder com imagem ?', default=False)
    video = models.FileField(upload_to='video/', storage=upload_storage, default="media/none.mp4")


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
    video = models.FileField(upload_to='video/', storage=upload_storage, default="media/none.mp4")
    aprendiz = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='aluno', related_name='respostaAluno', on_delete=models.CASCADE)
    # aprendiz = models.ForeignKey(Student, verbose_name='aprendiz ', related_name='respostaAprendiz', on_delete=models.CASCADE)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)


    def __str__(self):
        return self.edp.titulo + " - " + self.aprendiz.username
    
    def iniciar(self):
        self.save()
    @models.permalink
    def get_absolute_url(self):
        return ('edp:detalhe_edp_resposta', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Resposta Estrutura Digital de Aprendizagem'
        verbose_name_plural = 'Resposta Estrutura Digital de Aprendizagem'
        ordering = ['-created_at']

