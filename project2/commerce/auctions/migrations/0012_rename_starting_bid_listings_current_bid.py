# Generated by Django 5.1.3 on 2024-12-09 05:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0011_watchlist"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listings",
            old_name="starting_bid",
            new_name="current_bid",
        ),
    ]