# Generated by Django 4.2.3 on 2023-08-22 22:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0017_alter_content_object_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="object_id",
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
