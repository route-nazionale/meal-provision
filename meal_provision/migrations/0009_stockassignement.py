# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_provision', '0008_delete_stockassignement'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockAssignement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit', models.ForeignKey(to='meal_provision.Unit', to_field='id')),
                ('stock', models.ForeignKey(to='meal_provision.Stock', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
