# Generated by Django 2.0.5 on 2018-06-30 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edp', '0022_auto_20180630_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='resposta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='video_pk', to='edp.RespostaEdp', verbose_name='Video_resposta'),
            preserve_default=False,
        ),
    ]