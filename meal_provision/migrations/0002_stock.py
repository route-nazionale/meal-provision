# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        (b'meal_provision', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'letter', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator(b'[A-Z]{1}')])),
                (b'box_number', models.IntegerField()),
                (b'storeroom', models.ForeignKey(to=b'meal_provision.Storeroom', to_field='id')),
                (b'quartier', models.ForeignKey(to=b'meal_provision.Quartier', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
