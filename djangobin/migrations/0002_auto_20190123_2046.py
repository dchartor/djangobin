# Generated by Django 2.1.5 on 2019-01-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='tags',
            field=models.ManyToManyField(blank=True, to='djangobin.Tag'),
        ),
    ]
