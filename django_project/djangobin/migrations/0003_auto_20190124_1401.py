# Generated by Django 2.1.5 on 2019-01-24 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', '0002_auto_20190123_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='lang_code',
            field=models.CharField(max_length=100, unique=True, verbose_name='Language Code'),
        ),
    ]