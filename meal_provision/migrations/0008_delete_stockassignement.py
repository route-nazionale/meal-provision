# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_provision', '0007_auto_20140616_1646'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StockAssignement',
        ),
    ]
