# Generated by Django 2.1.1 on 2018-10-08 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DepotDoc', '0013_auto_20181008_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formation',
            old_name='niveaus',
            new_name='niveaux',
        ),
    ]