# Generated by Django 4.1.7 on 2023-03-14 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='budget',
            name='budget_start_date',
            field=models.DateField(),
        ),
    ]