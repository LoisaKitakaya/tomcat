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
                "verbose_name": "target",
                "verbose_name_plural": "targets",
                "db_table": "Targets",
                "ordering": ["-created_at"],
            },
        ),
    ]
