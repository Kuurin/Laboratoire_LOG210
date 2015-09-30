# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=120, null=True)),
                ('adresse', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DescriptionLivre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ISBN', models.CharField(max_length=16, null=True)),
                ('titre', models.CharField(max_length=120, null=True)),
                ('auteur', models.CharField(max_length=120, null=True)),
                ('nb_pages', models.IntegerField()),
                ('prix_neuf', models.CharField(max_length=14, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('email', models.EmailField(max_length=254, blank=True, null=True)),
                ('no_tel', models.CharField(max_length=20, blank=True, null=True)),
                ('password', models.CharField(max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gestionnaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ISBN', models.CharField(max_length=16, null=True)),
                ('etat', models.CharField(default='0.75', max_length=4, choices=[('0.75', 'Comme neuf'), ('0.50', 'Peu usé'), ('0.25', 'Très usé')])),
            ],
        ),
    ]
