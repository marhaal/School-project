# Generated by Django 2.0.13 on 2019-03-26 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0005_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='3.jpg', upload_to='profile_image/'),
        ),
    ]
