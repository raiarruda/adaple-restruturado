from django.db import models
from django.contrib.auth.models import User
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
