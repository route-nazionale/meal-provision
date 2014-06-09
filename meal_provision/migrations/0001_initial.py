# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Quartier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                (b'color', models.CharField(max_length=50)),
                (b'storerooms_number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'VirtualPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'from_day', models.IntegerField(default=1)),
                (b'to_day', models.IntegerField(default=1)),
                (b'from_meal', models.IntegerField(default=0)),
                (b'to_meal', models.IntegerField(default=2)),
                (b'std_meal', models.CharField(default=b'standard', max_length=50)),
                (b'col', models.CharField(default=b'latte', max_length=20)),
                (b'to_camst', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Storeroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'quartier', models.ForeignKey(to=b'meal_provision.Quartier', to_field='id')),
                (b'number', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
