# Generated by Django 4.1.7 on 2023-03-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_account_public_id_alter_budget_public_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='public_id',
            field=models.CharField(default='d3fa82f6a7ea48678fd326dc0d82a051', max_length=40),
        ),
        migrations.AlterField(
            model_name='budget',
            name='public_id',
            field=models.CharField(default='82f46c8431054c34afecc2e3fb6f8fdc', max_length=40),
        ),
        migrations.AlterField(
            model_name='category',
            name='public_id',
            field=models.CharField(default='a11f22eb669e493f88ab0ecbc90981a7', max_length=40),
        ),
        migrations.AlterField(
            model_name='report',
            name='public_id',
            field=models.CharField(default='b8159d36999a4296a312a8896234642b', max_length=40),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='public_id',
            field=models.CharField(default='74fdc607578b47e48135a87390ad44d7', max_length=40),
        ),
    ]
