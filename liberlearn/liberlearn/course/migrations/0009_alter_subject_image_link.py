# Generated by Django 4.2.3 on 2023-08-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0008_alter_subject_image_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="image_link",
            field=models.CharField(
                default="https://i.imgur.com/Z5DoxmH.png", max_length=200
            ),
        ),
    ]
