# Generated by Django 4.0.4 on 2022-05-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_voto_votacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='candidato',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='voto',
            name='votante',
            field=models.IntegerField(),
        ),
    ]