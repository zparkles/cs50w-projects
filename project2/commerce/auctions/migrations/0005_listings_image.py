# Generated by Django 5.1.3 on 2024-12-06 05:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_remove_listings_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="image",
            field=models.ImageField(blank=True, upload_to="images/"),
        ),
    ]
