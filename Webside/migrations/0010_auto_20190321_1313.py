# Generated by Django 2.0.13 on 2019-03-21 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0009_contact_issue_alternative'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='issue',
            new_name='issue_text',
        ),
    ]