# Generated by Django 4.1.7 on 2023-04-28 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trivial_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tiene",
            name="enUso",
            field=models.IntegerField(default=0),
        ),
    ]
