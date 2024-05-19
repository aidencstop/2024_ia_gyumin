# Generated by Django 4.2.10 on 2024-03-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0003_remove_activity_category_activity_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[("manager", "Manager"), ("counselor", "Counselor")],
                max_length=20,
            ),
        ),
    ]