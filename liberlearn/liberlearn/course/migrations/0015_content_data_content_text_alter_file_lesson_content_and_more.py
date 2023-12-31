# Generated by Django 4.2.3 on 2023-08-22 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0014_file_lesson_content_image_lesson_content_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="data",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="content",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="file",
            name="lesson_content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_content",
                to="course.content",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="lesson_content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_content",
                to="course.content",
            ),
        ),
        migrations.AlterField(
            model_name="text",
            name="lesson_content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_content",
                to="course.content",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="lesson_content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_content",
                to="course.content",
            ),
        ),
    ]
