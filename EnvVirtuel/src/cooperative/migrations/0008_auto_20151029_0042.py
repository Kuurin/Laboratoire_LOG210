# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0007_argent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='argent',
            old_name='user',
            new_name='username',
        ),
    ]
