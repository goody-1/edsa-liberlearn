# Generated by Django 4.2.3 on 2023-07-20 14:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_remove_user_is_facility_remove_user_is_mentor_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="facility",
            options={"verbose_name": "Facility", "verbose_name_plural": "Facilities"},
        ),
        migrations.AlterModelOptions(
            name="mentor",
            options={"verbose_name": "Mentor", "verbose_name_plural": "Mentors"},
        ),
        migrations.AlterModelOptions(
            name="student",
            options={"verbose_name": "Student", "verbose_name_plural": "Students"},
        ),
    ]
