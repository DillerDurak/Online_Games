# Generated by Django 3.2.9 on 2022-06-27 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20220624_2132'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Game',
            new_name='Game_tic',
        ),
        migrations.RenameModel(
            old_name='Player',
            new_name='Player_tic',
        ),
    ]
