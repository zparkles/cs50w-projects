# Generated by Django 5.1.3 on 2024-12-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0008_bid_bid_object_comment_comment_object"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]