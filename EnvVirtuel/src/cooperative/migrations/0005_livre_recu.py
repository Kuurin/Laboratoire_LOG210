# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0004_auto_20151024_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='recu',
            field=models.CharField(max_length=4, default='0', choices=[('0.75', 'Comme neuf'), ('0.50', 'Peu usé'), ('0.25', 'Très usé')]),
        ),
    ]
