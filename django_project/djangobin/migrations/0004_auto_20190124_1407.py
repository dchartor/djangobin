# Generated by Django 2.1.5 on 2019-01-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', '0003_auto_20190124_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='highlighted_code',
            field=models.TextField(blank=True, help_text='Read only field. Will contain the                                     syntax-highlited version of the original code.'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='hits',
            field=models.IntegerField(default=0, help_text='Read only field. Willd be upadted after every visit to snippet.'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='slug',
            field=models.SlugField(help_text='Read only field. Will be updated automatically.'),
        ),
    ]
