# Generated by Django 2.0.5 on 2018-07-17 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edp', '0007_respostaedp_aprendiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respostaedp',
            name='aprendiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostaAluno', to=settings.AUTH_USER_MODEL, verbose_name='aluno'),
        ),
    ]
