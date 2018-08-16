from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    eh_aluno = models.BooleanField(default=False)
    eh_professor = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username