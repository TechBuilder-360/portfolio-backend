# Generated by Django 3.1.1 on 2021-01-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_template_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='file',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
