# Generated by Django 4.1.7 on 2023-06-06 01:38

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlanBilling",
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
                ("order_tracking_id", models.CharField(max_length=200)),
                ("merchant_ref", models.CharField(max_length=50)),
                ("account_ref", models.CharField(blank=True, max_length=50)),
                ("redirect_url", models.URLField()),
                ("plan", models.CharField(max_length=10)),
                ("currency", models.CharField(max_length=5)),
                ("amount", models.FloatField(default=0.0)),
                ("payment_confirmed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "subscription payment",
                "verbose_name_plural": "subscription payments",
                "db_table": "SubscriptionPayments",
                "ordering": ["-created_at"],
            },
        ),
    ]
