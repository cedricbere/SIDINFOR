# Generated by Django 2.1.1 on 2018-10-07 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rapport', '0036_auto_20181007_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personne',
            name='nom',
            field=models.CharField(max_length=30, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='personne',
            name='prenom',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
        ),
    ]
