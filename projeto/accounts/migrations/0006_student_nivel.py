# Generated by Django 2.0.5 on 2018-10-26 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_assuntos'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='nivel',
            field=models.IntegerField(blank=True, default=0, verbose_name='Nível de proficiência'),
        ),
    ]
