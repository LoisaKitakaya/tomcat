# Generated by Django 4.1.7 on 2023-03-07 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_id',
            field=models.CharField(default='31825196fbe643d9a42bf3c0ef55cf15', max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='public_id',
            field=models.CharField(default='c6d67fda975b40c489d03748a81cfd8e', max_length=40),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='public_id',
            field=models.CharField(default='95a1674395eb42859778ab3b7f46d8a8', max_length=40),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='public_id',
            field=models.CharField(default='f8d579ccf18d47fb85c9278a424b9a89', max_length=40),
        ),
    ]
