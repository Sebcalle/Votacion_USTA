# Generated by Django 4.0.4 on 2022-05-21 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_voto_votacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voto',
            name='votacion',
        ),
    ]
