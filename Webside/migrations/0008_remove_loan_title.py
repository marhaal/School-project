# Generated by Django 2.1.5 on 2019-02-24 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0007_comment2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='title',
        ),
    ]