# Generated by Django 5.0.7 on 2024-08-26 14:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.AddField(
            model_name="fooditem",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
    ]