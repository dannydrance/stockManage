# Generated by Django 5.1 on 2025-02-27 03:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stoke", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="last_consumed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="restock_threshold",
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name="product",
            name="sold_number",
            field=models.IntegerField(default=0),
        ),
    ]
