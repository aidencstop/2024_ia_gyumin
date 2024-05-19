# Generated by Django 4.2.10 on 2024-03-04 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0004_remove_student_activity_remove_student_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="name",
            field=models.TextField(default="noname", max_length=60),
        ),
        migrations.AlterField(
            model_name="student",
            name="grade",
            field=models.IntegerField(
                choices=[
                    (10, "Grade 10"),
                    (11, "Grade 11"),
                    (12, "Grade 12"),
                    (13, "Grade 13"),
                ]
            ),
        ),
    ]
