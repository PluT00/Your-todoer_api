# Generated by Django 3.1.3 on 2020-11-08 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('your_todoer_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='user',
            new_name='owner',
        ),
    ]
