# Generated by Django 2.2.8 on 2020-09-04 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200904_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pix',
            field=models.URLField(verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='resume',
            field=models.URLField(verbose_name='resume'),
        ),
    ]
