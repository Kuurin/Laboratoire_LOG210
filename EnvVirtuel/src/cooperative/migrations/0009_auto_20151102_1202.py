# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0008_auto_20151029_0042'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Etudiant',
        ),
        migrations.DeleteModel(
            name='Gestionnaire',
        ),
        migrations.AlterField(
            model_name='livre',
            name='recu',
            field=models.CharField(choices=[('0', 'Avec le vendeur'), ('0.25', 'A la cooperative'), ('0.50', 'Reserve'), ('0.75', 'Achete'), ('1', "Delivre à l'acheteur")], max_length=4, default='0'),
        ),
    ]
