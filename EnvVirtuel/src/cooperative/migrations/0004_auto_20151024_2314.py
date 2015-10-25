# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0003_livre_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livre',
            name='user',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
