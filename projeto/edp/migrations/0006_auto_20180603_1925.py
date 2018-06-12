# Generated by Django 2.0.5 on 2018-06-03 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edp', '0005_auto_20180603_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='edp',
            name='habilidade_audicao',
            field=models.BooleanField(default=False, verbose_name='Audição'),
        ),
        migrations.AddField(
            model_name='edp',
            name='habilidade_escrita',
            field=models.BooleanField(default=False, verbose_name='Escrita'),
        ),
        migrations.AddField(
            model_name='edp',
            name='habilidade_fala',
            field=models.BooleanField(default=False, verbose_name='Fala'),
        ),
        migrations.AddField(
            model_name='edp',
            name='habilidade_leitura',
            field=models.BooleanField(default=False, verbose_name='Leitura'),
        ),
        migrations.AddField(
            model_name='edp',
            name='habilidade_traducao',
            field=models.BooleanField(default=False, verbose_name='Tradução'),
        ),
    ]