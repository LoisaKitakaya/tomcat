# Generated by Django 4.1.7 on 2023-06-04 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("transactions", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
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
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.account",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="transactions.transactioncategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "budget",
                "verbose_name_plural": "budgets",
                "db_table": "Budgets",
                "ordering": ["-created_at"],
            },
        ),
    ]