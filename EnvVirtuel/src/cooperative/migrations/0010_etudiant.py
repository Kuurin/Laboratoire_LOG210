# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20151024_2157'),
        ('cooperative', '0009_auto_20151102_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL, parent_link=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
