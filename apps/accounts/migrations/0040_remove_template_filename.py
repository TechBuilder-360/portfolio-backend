# Generated by Django 3.1.1 on 2021-01-29 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_auto_20210129_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='filename',
        ),
    ]
