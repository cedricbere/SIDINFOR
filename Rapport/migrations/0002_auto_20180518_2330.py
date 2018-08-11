# Generated by Django 2.0.4 on 2018-05-18 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Rapport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soutenance',
            name='dateEffectif',
        ),
        migrations.AddField(
            model_name='soutenance',
            name='dateEffective',
            field=models.DateField(null=True, verbose_name='Date effective'),
        ),
        migrations.AlterField(
            model_name='classe',
            name='nom_classe',
            field=models.CharField(max_length=20, unique=True, verbose_name='Classe'),
        ),
        migrations.AlterField(
            model_name='compte',
            name='actif',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='compte',
            name='dPassword',
            field=models.CharField(max_length=30, verbose_name='Confirmez le mot de passe'),
        ),
        migrations.AlterField(
            model_name='compte',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Adresse électronique'),
        ),
        migrations.AlterField(
            model_name='compte',
            name='password',
            field=models.CharField(max_length=30, verbose_name='Mot de Passe'),
        ),
        migrations.AlterField(
            model_name='departement',
            name='nom_dpt',
            field=models.CharField(max_length=50, verbose_name='Département'),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='dateNaissance',
            field=models.DateField(verbose_name='Date de Naissance'),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='filiere',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Rapport.Filiere', verbose_name='Filière'),
        ),
        migrations.AlterField(
            model_name='filiere',
            name='nom_filiere',
            field=models.CharField(max_length=50, verbose_name='Filière'),
        ),
        migrations.AlterField(
            model_name='personne',
            name='nom',
            field=models.CharField(max_length=30, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='personne',
            name='numTel',
            field=models.CharField(max_length=25, null=True, unique=True, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='personne',
            name='prenom',
            field=models.CharField(max_length=30, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='rapport',
            name='anneAcademique',
            field=models.CharField(max_length=30, verbose_name='Année académique'),
        ),
        migrations.AlterField(
            model_name='rapport',
            name='resume',
            field=models.TextField(verbose_name='Résumé'),
        ),
        migrations.AlterField(
            model_name='rapport',
            name='theme',
            field=models.CharField(max_length=200, verbose_name='Thème'),
        ),
        migrations.AlterField(
            model_name='soutenance',
            name='datePrevu',
            field=models.DateField(null=True, verbose_name='Date de Soutenance'),
        ),
        migrations.AlterField(
            model_name='soutenance',
            name='pv',
            field=models.CharField(max_length=200, verbose_name='Procès verbal'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='etat',
            field=models.CharField(max_length=20, verbose_name='État'),
        ),
        migrations.AlterField(
            model_name='ufr',
            name='nom_ufr',
            field=models.CharField(max_length=50, unique=True, verbose_name='UFR'),
        ),
    ]
