# Generated by Django 2.0.13 on 2019-03-19 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0004_auto_20190315_1244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='user1',
            new_name='giver',
        ),
        migrations.RenameField(
            model_name='trade',
            old_name='user2',
            new_name='receiver',
        ),
    ]
