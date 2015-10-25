# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DescriptionLivre',
        ),
        migrations.AddField(
            model_name='livre',
            name='auteur',
            field=models.CharField(null=True, max_length=120),
        ),
        migrations.AddField(
            model_name='livre',
            name='nb_pages',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='livre',
            name='prix_neuf',
            field=models.CharField(null=True, max_length=14),
        ),
        migrations.AddField(
            model_name='livre',
            name='titre',
            field=models.CharField(null=True, max_length=120),
        ),
    ]
