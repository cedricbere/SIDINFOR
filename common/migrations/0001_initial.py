# Generated by Django 2.1.3 on 2018-12-09 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_classe', models.CharField(max_length=20, unique=True, verbose_name='Classe')),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_dpt', models.CharField(max_length=50, verbose_name='Département')),
            ],
        ),
        migrations.CreateModel(
            name='Filiere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_filiere', models.CharField(max_length=50, verbose_name='Filière')),
                ('dpt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Departement')),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credits', models.IntegerField(verbose_name='Crédits')),
                ('nom_matiere', models.CharField(max_length=100, verbose_name='Nom de la matière')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=30, verbose_name='Prénom')),
                ('sexe', models.CharField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme', max_length=5)),
                ('dateNaissance', models.DateField(blank=True, null=True, verbose_name='Date de Naissance')),
                ('numTel', models.CharField(blank=True, max_length=25, null=True, unique=True, verbose_name='Téléphone')),
            ],
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_semestre', models.CharField(max_length=15, unique=True, verbose_name='Semestre')),
                ('niveau', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Classe')),
            ],
        ),
        migrations.CreateModel(
            name='UFR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_ufr', models.CharField(max_length=50, unique=True, verbose_name='UFR')),
            ],
        ),
        migrations.CreateModel(
            name='UniteEnseignement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=11, null=True, unique=True)),
                ('nom_unite', models.CharField(max_length=100, verbose_name="Unité d'enseignement")),
                ('semestre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Semestre')),
            ],
        ),
        migrations.AddField(
            model_name='matiere',
            name='ue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.UniteEnseignement', verbose_name="Unité d'enseignement"),
        ),
        migrations.AddField(
            model_name='departement',
            name='ufr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.UFR'),
        ),
    ]