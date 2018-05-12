from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from projeto.accounts.models import Student, assuntos
from django.db import transaction

from django.contrib.auth import get_user_model
User = get_user_model()

class CadastroAlunoForm(UserCreationForm):
  #  a =  forms.ModelMultipleChoiceField(
    #     queryset= assuntos.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
        
    # )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.eh_aluno = True
        user.save()
        student = Student.objects.create(user=user)
#        student.a.add(*self.cleaned_data.get('a'))

        return user
        

class CadastroProfessorForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.eh_professor = True
        if commit:
            user.save()
        return user