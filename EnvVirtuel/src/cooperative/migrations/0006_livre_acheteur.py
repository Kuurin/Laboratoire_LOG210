# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0005_livre_recu'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='acheteur',
            field=models.CharField(null=True, default='', max_length=120, blank=True),
        ),
    ]
