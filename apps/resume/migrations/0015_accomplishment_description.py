# Generated by Django 3.1.1 on 2021-01-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0014_accomplishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomplishment',
            name='description',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
