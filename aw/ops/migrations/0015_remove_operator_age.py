# Generated by Django 3.1.1 on 2020-12-07 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0014_auto_20201207_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operator',
            name='age',
        ),
    ]
