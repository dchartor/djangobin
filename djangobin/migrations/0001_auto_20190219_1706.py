# Generated by Django 2.1.5 on 2019-02-19 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', 'language_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='hits',
            field=models.IntegerField(default=0, help_text='Read only field. Willd be updated after every visit to snippet.'),
        ),
    ]
