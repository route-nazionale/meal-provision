# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'meal_provision', b'0003_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'code', models.IntegerField()),
                (b'unit', models.ForeignKey(to=b'meal_provision.Unit', to_field='id')),
                (b'tipo_codice', models.CharField(max_length=50)),
                (b'intolleranze_allergie', models.CharField(max_length=100, null=True)),
                (b'std_meal', models.CharField(default=b'standard', max_length=50)),
                (b'col', models.CharField(default=b'latte', max_length=20)),
                (b'from_day', models.IntegerField(default=1)),
                (b'to_day', models.IntegerField(default=1)),
                (b'from_meal', models.IntegerField(default=0)),
                (b'to_meal', models.IntegerField(default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
