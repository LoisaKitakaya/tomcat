# Generated by Django 4.1.7 on 2023-03-09 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(default='a461823a163040cda98b7a093930ee3f', max_length=40)),
                ('account_name', models.CharField(max_length=100)),
                ('account_type', models.CharField(choices=[('checking', 'Checking'), ('saving', 'Saving'), ('credit', 'Credit'), ('investment', 'Investment'), ('retirement', 'Retirement'), ('loan', 'Loan'), ('insurance', 'Insurance'), ('mortgage', 'Mortgage')], default='checking', max_length=50)),
                ('currency_code', models.CharField(max_length=3)),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
                'db_table': 'Accounts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(default='bced612c64b348f4a4238d5f9598f815', max_length=40)),
                ('category_name', models.CharField(max_length=100)),
                ('category_description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(default='723dabbf5e3046cdbd107c11694847d7', max_length=40)),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer'), ('payment', 'Payment')], max_length=50)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency_code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=255)),
                ('transaction_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
                'db_table': 'Transactions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(default='6b9db9391f954a50a0166afb0beaaaba', max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account')),
                ('transactions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.transaction')),
            ],
            options={
                'verbose_name': 'report',
                'verbose_name_plural': 'reports',
                'db_table': 'Reports',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(default='4d74ceea96234a358c96358edfe7772d', max_length=40)),
                ('budget_name', models.CharField(max_length=100)),
                ('budget_description', models.CharField(max_length=255)),
                ('budget_start_date', models.DateTimeField()),
                ('budget_end_date', models.DateTimeField()),
                ('budget_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
            options={
                'verbose_name': 'budget',
                'verbose_name_plural': 'budgets',
                'db_table': 'Budgets',
                'ordering': ['-created_at'],
            },
        ),
    ]
