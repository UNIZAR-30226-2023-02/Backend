# Generated by Django 4.1.7 on 2023-05-11 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sala", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PeticionesAmigo",
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
                (
                    "peticion_amigo",
                    models.ForeignKey(
                        db_column="amigo_inv",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="amigo_inv",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sala_inv",
                    models.ForeignKey(
                        db_column="sala_invitado",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sala_invitado",
                        to="sala.sala",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "Peticiones",
            },
        ),
    ]