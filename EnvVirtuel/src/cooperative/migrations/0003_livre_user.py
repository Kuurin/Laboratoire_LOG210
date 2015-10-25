# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooperative', '0002_auto_20151024_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
        ),
    ]
