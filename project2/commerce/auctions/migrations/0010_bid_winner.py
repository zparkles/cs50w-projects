# Generated by Django 5.1.3 on 2024-12-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0009_listings_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="winner",
            field=models.BooleanField(default=False),
        ),
    ]