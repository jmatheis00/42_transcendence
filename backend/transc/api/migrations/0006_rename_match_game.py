# Generated by Django 4.2.7 on 2023-12-17 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_user_id_match_player_id_match_player2_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Match',
            new_name='Game',
        ),
    ]
