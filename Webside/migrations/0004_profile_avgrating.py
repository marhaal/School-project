# Generated by Django 2.0.13 on 2019-03-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0003_auto_20190321_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avgrating',
            field=models.IntegerField(default=0),
        ),
    ]
