# Generated by Django 3.1.1 on 2020-12-07 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0002_race'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='race',
            field=models.ForeignKey(default=35, on_delete=django.db.models.deletion.CASCADE, to='ops.race'),
        ),
    ]