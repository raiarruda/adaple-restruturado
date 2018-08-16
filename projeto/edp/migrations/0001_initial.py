# Generated by Django 2.0.5 on 2018-07-17 21:10

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Edp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('slug', models.SlugField(verbose_name='Atalho')),
                ('objetivo_pedagogico', models.TextField(verbose_name='Objetivo Pegagogico')),
                ('atividades', models.TextField(verbose_name='Atividades')),
                ('metodologia', models.TextField(verbose_name='Metodologia')),
                ('nivel', models.IntegerField(blank=True, choices=[(0, 'Básico (Sem certificação)'), (1, 'Intermediário'), (2, 'Intermediário Superior'), (3, 'Avançado'), (4, 'Avançado Superior')], default=0, verbose_name='Nível de proficiência')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Estrutura Digital de Aprendizagem',
                'verbose_name_plural': 'Estruturas Digital de Aprendizagem',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Habilidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RecursosEdp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_embedded', embed_video.fields.EmbedVideoField(blank=True, null=True)),
                ('texto', models.TextField(blank=True, verbose_name='Texto')),
                ('recebe_texto', models.BooleanField(default=False, verbose_name='Responder texto ?')),
                ('recebe_video_embedded', models.BooleanField(default=False, verbose_name='Responder com videos do youtube?')),
                ('recebe_video', models.BooleanField(default=False, verbose_name='Responder com video?')),
                ('recebe_imagem', models.BooleanField(default=False, verbose_name='Responder com imagem ?')),
                ('video', models.FileField(default='media/none.mp4', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\raiss\\Documents\\Projetos\\startbootstrap-sb-admin-2\\adaple-restruturado\\projeto\\static'), upload_to='video/')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('edp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recursos', to='edp.Edp', verbose_name='Edp')),
            ],
            options={
                'verbose_name': 'Recurso Estrutura Digital de Aprendizagem',
                'verbose_name_plural': 'Recursos Estruturas  Digital de Aprendizagem',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='RespostaEdp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_embedded', embed_video.fields.EmbedVideoField(blank=True, null=True)),
                ('texto', models.TextField(blank=True, verbose_name='Texto')),
                ('video', models.FileField(default='media/none.mp4', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\raiss\\Documents\\Projetos\\startbootstrap-sb-admin-2\\adaple-restruturado\\projeto\\static'), upload_to='video/')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('edp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='edp.Edp', verbose_name='Edp')),
            ],
            options={
                'verbose_name': 'Resposta Estrutura Digital de Aprendizagem',
                'verbose_name_plural': 'Resposta Estrutura Digital de Aprendizagem',
                'ordering': ['edp'],
            },
        ),
        migrations.AddField(
            model_name='edp',
            name='habilidades',
            field=models.ManyToManyField(related_name='habilidade_edp', to='edp.Habilidade'),
        ),
        migrations.AddField(
            model_name='edp',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edps', to=settings.AUTH_USER_MODEL),
        ),
    ]
