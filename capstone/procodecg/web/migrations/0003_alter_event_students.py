# Generated by Django 5.1.3 on 2025-01-02 08:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0002_alter_event_students"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="students",
            field=models.ManyToManyField(
                blank=True, related_name="schedule", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
