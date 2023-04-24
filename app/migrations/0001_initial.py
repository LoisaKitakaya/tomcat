# Generated by Django 4.1.7 on 2023-04-24 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_name", models.CharField(max_length=100)),
                ("account_type", models.CharField(max_length=50)),
                ("currency_code", models.CharField(max_length=3)),
                ("account_balance", models.FloatField(default=0.0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "account",
                "verbose_name_plural": "accounts",
                "db_table": "Accounts",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("budget_name", models.CharField(max_length=100)),
                ("budget_description", models.TextField()),
                ("budget_is_active", models.BooleanField(default=True)),
                ("budget_amount", models.FloatField(default=0.0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "budget",
                "verbose_name_plural": "budgets",
                "db_table": "Budgets",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=150)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("phone_number", models.CharField(max_length=20)),
                ("ID_number", models.CharField(max_length=100)),
                ("employment_status", models.CharField(max_length=20)),
                ("job_title", models.CharField(max_length=255)),
                ("job_description", models.TextField()),
                ("is_manager", models.BooleanField(default=False)),
                ("salary", models.FloatField(default=0.0)),
                ("department", models.CharField(max_length=255)),
                ("employee_id", models.CharField(max_length=50)),
                ("emergency_contact_name", models.CharField(max_length=50)),
                ("emergency_contact_phone_number", models.CharField(max_length=20)),
                (
                    "emergency_contact_email",
                    models.EmailField(blank=True, max_length=150),
                ),
                ("date_of_hire", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "employee",
                "verbose_name_plural": "employees",
                "db_table": "Employees",
                "ordering": ["-date_of_hire"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("buying_price", models.FloatField(default=0.0)),
                ("selling_price", models.FloatField(default=0.0)),
                ("current_stock_level", models.IntegerField(default=0)),
                ("units_sold", models.IntegerField(default=0)),
                ("reorder_level", models.IntegerField(blank=True, default=0)),
                ("reorder_quantity", models.IntegerField(blank=True, default=0)),
                ("supplier_name", models.CharField(max_length=255)),
                ("supplier_phone_number", models.CharField(max_length=20)),
                ("supplier_email", models.CharField(blank=True, max_length=150)),
                ("profit_generated", models.FloatField(blank=True, default=0.0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "product",
                "verbose_name_plural": "products",
                "db_table": "Products",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=100, unique=True)),
                ("category_description", models.TextField()),
            ],
            options={
                "verbose_name": "product category",
                "verbose_name_plural": "product categories",
                "db_table": "ProductCategories",
            },
        ),
        migrations.CreateModel(
            name="ProductSubCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=100, unique=True)),
                ("category_description", models.TextField()),
            ],
            options={
                "verbose_name": "product sub category",
                "verbose_name_plural": "product sub categories",
                "db_table": "ProductSubCategories",
            },
        ),
        migrations.CreateModel(
            name="TransactionCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=100, unique=True)),
                ("category_description", models.TextField()),
            ],
            options={
                "verbose_name": "transaction category",
                "verbose_name_plural": "transaction categories",
                "db_table": "TransactionCategories",
            },
        ),
        migrations.CreateModel(
            name="TransactionType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_name", models.CharField(max_length=100, unique=True)),
                ("type_description", models.TextField()),
            ],
            options={
                "verbose_name": "transaction type",
                "verbose_name_plural": "transaction types",
                "db_table": "TransactionTypes",
            },
        ),
        migrations.CreateModel(
            name="TransactionSubCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=100, unique=True)),
                ("category_description", models.TextField()),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.transactioncategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "transaction sub category",
                "verbose_name_plural": "transaction sub categories",
                "db_table": "TransactionSubCategories",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transaction_amount", models.FloatField(default=0.0)),
                ("currency_code", models.CharField(max_length=3)),
                ("description", models.TextField()),
                ("transaction_date", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.account"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.transactioncategory",
                    ),
                ),
                (
                    "sub_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.transactionsubcategory",
                    ),
                ),
                (
                    "transaction_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.transactiontype",
                    ),
                ),
            ],
            options={
                "verbose_name": "transaction",
                "verbose_name_plural": "transactions",
                "db_table": "Transactions",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Target",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("target_name", models.CharField(max_length=100)),
                ("target_description", models.TextField()),
                ("target_is_active", models.BooleanField(default=True)),
                ("target_amount", models.FloatField(default=0.0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.account"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.transactioncategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "target",
                "verbose_name_plural": "targets",
                "db_table": "Targets",
                "ordering": ["-created_at"],
            },
        ),
    ]
