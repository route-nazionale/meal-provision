# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'meal_provision', b'0002_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'vclan', models.CharField(max_length=30)),
                (b'vclanID', models.CharField(max_length=30)),
                (b'unitaID', models.CharField(default=b'T1', max_length=30)),
                (b'gruppoID', models.CharField(max_length=30)),
                (b'quartier', models.ForeignKey(to=b'meal_provision.Quartier', to_field='id')),
                (b'storeroom', models.ForeignKey(to=b'meal_provision.Storeroom', to_field='id')),
                (b'stock', models.ForeignKey(to=b'meal_provision.Stock', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
