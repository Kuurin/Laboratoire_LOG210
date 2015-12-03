# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0010_etudiant'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='tempsReserve',
            field=models.FloatField(default=0),
        ),
    ]
