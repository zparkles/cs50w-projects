# Generated by Django 5.1.3 on 2024-12-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_listings_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listings",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]