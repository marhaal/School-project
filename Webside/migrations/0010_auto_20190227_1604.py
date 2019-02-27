# Generated by Django 2.0.13 on 2019-02-27 15:04

from django.db import migrations, models
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Webside', '0009_auto_20190224_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('address', django_google_maps.fields.AddressField(max_length=200)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=7, null=True)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=7, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
