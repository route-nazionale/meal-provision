# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'meal_provision', b'0004_person'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'CamstControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'to_camst', models.BooleanField(default=True)),
                (b'person', models.ForeignKey(to=b'meal_provision.Person', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
