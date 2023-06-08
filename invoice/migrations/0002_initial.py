# Generated by Django 4.1.7 on 2023-06-06 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("invoice", "0001_initial"),
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentaccount",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="business",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="invoice.paymentaccount"
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="transactions.transactioncategory",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="invoice.clientinformation",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="sub_category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="transactions.transactionsubcategory",
            ),
        ),
        migrations.AddField(
            model_name="clientinformation",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.profile"
            ),
        ),
    ]