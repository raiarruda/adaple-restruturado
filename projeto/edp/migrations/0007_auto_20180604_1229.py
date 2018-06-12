# Generated by Django 2.0.5 on 2018-06-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edp', '0006_auto_20180603_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edp',
            name='habilidade_audicao',
            field=models.BooleanField(verbose_name='Audição'),
        ),
        migrations.AlterField(
            model_name='edp',
            name='habilidade_escrita',
            field=models.BooleanField(verbose_name='Escrita'),
        ),
        migrations.AlterField(
            model_name='edp',
            name='habilidade_fala',
            field=models.BooleanField(verbose_name='Fala'),
        ),
        migrations.AlterField(
            model_name='edp',
            name='habilidade_leitura',
            field=models.BooleanField(verbose_name='Leitura'),
        ),
        migrations.AlterField(
            model_name='edp',
            name='habilidade_traducao',
            field=models.BooleanField(verbose_name='Tradução'),
        ),
    ]