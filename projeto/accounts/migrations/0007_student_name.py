# Generated by Django 2.0.5 on 2018-10-26 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_student_nivel'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
    ]