# Generated by Django 4.1.7 on 2023-05-07 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partida", "0003_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="partida",
            name="tiempo_respuesta",
            field=models.IntegerField(default=15),
        ),
    ]
