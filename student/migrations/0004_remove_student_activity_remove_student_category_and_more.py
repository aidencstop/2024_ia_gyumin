# Generated by Django 4.2.10 on 2024-02-26 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0003_alter_activityexperience_end_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="activity",
        ),
        migrations.RemoveField(
            model_name="student",
            name="category",
        ),
        migrations.RemoveField(
            model_name="student",
            name="description",
        ),
        migrations.RemoveField(
            model_name="student",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="student",
            name="start_date",
        ),
        migrations.RemoveField(
            model_name="student",
            name="user",
        ),
    ]
