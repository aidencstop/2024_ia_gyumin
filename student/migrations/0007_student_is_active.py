# Generated by Django 4.2.10 on 2024-04-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0006_alter_student_grade"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
