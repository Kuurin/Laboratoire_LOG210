# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0006_livre_acheteur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Argent',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('montant', models.CharField(null=True, max_length=120, blank=True)),
                ('user', models.CharField(null=True, max_length=120, blank=True)),
            ],
        ),
    ]
