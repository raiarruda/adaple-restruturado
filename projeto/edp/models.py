from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Habilidade (models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Edp(models.Model):
    
    titulo = models.CharField('Título', max_length=100)
    slug = models.SlugField('Atalho')
    objetivo_pedagogico = models.TextField('Objetivo Pegagogico')
  #  habilidades = models.ManyToManyField('Habilidades', Habilidade)
   # habilidades = ListCharField(
    #    base_field=models.CharField(max_length=10),
     #   size=6,
      #  max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    #)
    atividades = models.TextField('Atividades')
    metodologia = models.TextField('Metodologia')
    usuario = models.ForeignKey(User, related_name='edps', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def iniciar(self):
        self.save()

    def __str__(self):
        return self.titulo
    
    @models.permalink
    def get_absolute_url(self):
        return ('edp:detalhes_edp', (), {'slug': self.slug})

    
    class Meta:
        verbose_name = 'Estrutura Digital Pedagógica'
        verbose_name_plural = 'Estruturas Digitais Pedagógicas'
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

    #TODO descobrir a diferença usando isso
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
   
    edp = models.ForeignKey(Edp, verbose_name='Edp', related_name='edps', on_delete=models.CASCADE)
    video_embedded = models.TextField('Video embedded', blank=True)
    texto = models.TextField('Texto', blank=True)
    recebe_texto = models.BooleanField('Responder texto ?', default=False)
    recebe_video_embedded = models.BooleanField('Responder com videos do youtube?', default=False )
    recebe_video = models.BooleanField('Responder com video?', default=False)
    recebe_imagem = models.BooleanField('Responder com imagem ?', default=False)


    def __str__(self):
        return self.edp.titulo
    
    def iniciar(self):
        self.save()