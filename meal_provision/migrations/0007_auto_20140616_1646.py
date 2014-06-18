# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'meal_provision', b'0006_unit_size'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'StockAssignement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'unit', models.ForeignKey(to=b'meal_provision.Unit', to_field='id')),
                (b'stock', models.ForeignKey(to=b'meal_provision.Stock', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name=b'unit',
            name=b'stock',
        ),
    ]
