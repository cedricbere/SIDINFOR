# Generated by Django 2.1.1 on 2018-10-18 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Rapport', '0040_personne_datenaissance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapport',
            name='stage',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Rapport.Stage'),
        ),
        migrations.AlterField(
            model_name='soutenance',
            name='etudiant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Rapport.Etudiant'),
        ),
        migrations.AlterField(
            model_name='soutenance',
            name='stage',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Rapport.Stage'),
        ),
    ]