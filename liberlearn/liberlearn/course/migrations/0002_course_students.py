# Generated by Django 4.2.3 on 2023-07-27 15:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(
                blank=True, related_name="courses_joined", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
