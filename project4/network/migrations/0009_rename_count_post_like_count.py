# Generated by Django 5.1.3 on 2024-12-25 07:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0008_post_count"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="count",
            new_name="like_count",
        ),
    ]