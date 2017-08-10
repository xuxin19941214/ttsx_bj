# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_goods', '0002_auto_20170707_1910'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GoodsIndo',
            new_name='GoodsInfo',
        ),
    ]
