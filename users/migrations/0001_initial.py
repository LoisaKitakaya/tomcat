# Generated by Django 4.1.7 on 2023-03-30 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('accounts', models.BooleanField(default=False)),
                ('no_of_accounts', models.IntegerField(default=0)),
                ('budgets', models.BooleanField(default=False)),
                ('no_of_budgets', models.IntegerField(default=0)),
                ('targets', models.BooleanField(default=False)),
                ('no_of_targets', models.IntegerField(default=0)),
                ('pdf_reports', models.BooleanField(default=False)),
                ('ai_assistant', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'subscriber package',
                'verbose_name_plural': 'subscriber packages',
                'db_table': 'SubscriberPackages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workspace_uid', models.CharField(max_length=50)),
                ('is_employee', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
                'db_table': 'UserProfiles',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OTPDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('key', models.CharField(default='5BN4SW4CCJW2UH7BVP6M4WTMOALMHIGH', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user device',
                'verbose_name_plural': 'user devices',
                'db_table': 'UserDevices',
                'ordering': ['-created_at'],
            },
        ),
    ]
