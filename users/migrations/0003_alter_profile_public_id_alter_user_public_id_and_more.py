# Generated by Django 4.1.7 on 2023-03-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_public_id_alter_user_public_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_id',
            field=models.CharField(default='3cbf7e8f13d24016914c2dcffbde3eea', max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='public_id',
            field=models.CharField(default='7d526425edb74cc1b7654dc39e3b1267', max_length=40),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='public_id',
            field=models.CharField(default='2dbe2db825b0422ba5372080aa568890', max_length=40),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='public_id',
            field=models.CharField(default='6845dce3f1da4d73a404f28c6cecab25', max_length=40),
        ),
    ]
