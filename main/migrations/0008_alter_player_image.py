# Generated by Django 3.2.9 on 2022-06-17 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_game_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
