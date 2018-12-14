# Generated by Django 2.1.3 on 2018-12-11 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('depot_dossier', '0002_auto_20181209_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, unique=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='documentid',
            options={'verbose_name': 'Document ID', 'verbose_name_plural': 'Documents IDs'},
        ),
        migrations.AlterModelOptions(
            name='fichiers',
            options={'verbose_name': 'Pièces jointes', 'verbose_name_plural': 'Pièces jointes'},
        ),
    ]
