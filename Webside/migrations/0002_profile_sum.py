# Generated by Django 2.0.13 on 2019-03-21 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sum',
            field=models.IntegerField(default=0),
        ),
    ]
