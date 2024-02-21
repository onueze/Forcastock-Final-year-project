# Generated by Django 5.0.1 on 2024-02-07 01:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name="Project",
        ),
    ]