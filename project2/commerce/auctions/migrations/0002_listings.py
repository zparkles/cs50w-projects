# Generated by Django 5.1.3 on 2024-12-05 08:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Listings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("starting_bid", models.DecimalField(decimal_places=0, max_digits=12)),
                ("image", models.ImageField(blank=True, upload_to="images/")),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Fashion", "Fashion"),
                            ("Toys", "Toys"),
                            ("Electronics", "Electronics"),
                            ("Home", "Home"),
                            ("Others", "Others"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
