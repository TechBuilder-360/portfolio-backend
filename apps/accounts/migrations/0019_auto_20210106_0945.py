# Generated by Django 3.1.1 on 2021-01-06 08:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210106_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 6, 9, 45, 53, 410003)),
        ),
    ]
