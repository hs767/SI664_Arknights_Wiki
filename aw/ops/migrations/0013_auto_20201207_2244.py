# Generated by Django 3.1.1 on 2020-12-07 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0012_operator_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2),
        ),
    ]