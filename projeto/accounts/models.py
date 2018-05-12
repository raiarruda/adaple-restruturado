from django.contrib.auth.models import AbstractUser
from django.db import models



class assuntos(models.Model):
    nome = models.CharField(max_length=20)


    def __str__(self):
        return self.nome

class User(AbstractUser):
    eh_aluno = models.BooleanField(default=False)
    eh_professor = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  #  a = models.ManyToManyField(assuntos, related_name='a_assuntos')

