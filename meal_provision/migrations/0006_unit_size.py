# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'meal_provision', b'0005_camstcontrol'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'unit',
            name=b'size',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
