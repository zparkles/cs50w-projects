# Generated by Django 5.1.3 on 2024-12-05 14:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_listings"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listings",
            name="user",
        ),
        migrations.AddField(
            model_name="listings",
            name="author",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]