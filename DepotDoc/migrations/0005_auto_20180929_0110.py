# Generated by Django 2.1.1 on 2018-09-29 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DepotDoc', '0004_auto_20180928_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='niveau',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
