# Generated by Django 2.0.5 on 2018-07-12 04:58

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edp', '0002_remove_video_texto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recursosedp',
            name='video',
            field=models.FileField(default='media/none.mp4', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\raiss\\Documents\\Projetos\\startbootstrap-sb-admin-2\\adaple-restruturado\\projeto\\static'), upload_to='videos/'),
        ),
        migrations.AlterField(
            model_name='respostaedp',
            name='video',
            field=models.FileField(default='media/none.mp4', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\raiss\\Documents\\Projetos\\startbootstrap-sb-admin-2\\adaple-restruturado\\projeto\\static'), upload_to='video/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(default='media/none.mp4', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\raiss\\Documents\\Projetos\\startbootstrap-sb-admin-2\\adaple-restruturado\\projeto\\static'), upload_to='videos/'),
        ),
    ]
