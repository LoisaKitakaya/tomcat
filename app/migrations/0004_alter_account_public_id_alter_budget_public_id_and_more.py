# Generated by Django 4.1.7 on 2023-03-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_account_public_id_alter_budget_public_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='public_id',
            field=models.CharField(default='c6e0e2eb23f74daf90cad15403031944', max_length=40),
        ),
        migrations.AlterField(
            model_name='budget',
            name='public_id',
            field=models.CharField(default='e71fa3f534c1490fa17365139ad34364', max_length=40),
        ),
        migrations.AlterField(
            model_name='budgetcategory',
            name='public_id',
            field=models.CharField(default='4edf2c20b4b64089b138b8b2c4552c19', max_length=40),
        ),
        migrations.AlterField(
            model_name='category',
            name='public_id',
            field=models.CharField(default='ac0fe0ea92d543d1b4a31a2dc67cb72c', max_length=40),
        ),
        migrations.AlterField(
            model_name='report',
            name='public_id',
            field=models.CharField(default='d568a3ab4ffb4941a2c177acc9dbc8f5', max_length=40),
        ),
        migrations.AlterField(
            model_name='reportcategory',
            name='public_id',
            field=models.CharField(default='785b18842a494b9093aff8cad0f517c7', max_length=40),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='public_id',
            field=models.CharField(default='6acb73050f5945659e6f77d8f8cd4739', max_length=40),
        ),
        migrations.AlterField(
            model_name='transactioncategory',
            name='public_id',
            field=models.CharField(default='02c1885f5cce4508ac776daf34968b08', max_length=40),
        ),
    ]