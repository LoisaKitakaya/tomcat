# Generated by Django 4.1.7 on 2023-06-06 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("targets", "0001_initial"),
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="target",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="target",
            name="sub_category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="transactions.transactionsubcategory",
            ),
        ),
    ]
