# Generated by Django 4.1.7 on 2023-04-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_alter_workspace_workspace_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='workspace_uid',
            field=models.CharField(default='9c6e3eac38684905849099838faacf12', max_length=50),
        ),
    ]
