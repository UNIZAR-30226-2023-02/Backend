# Generated by Django 4.1.7 on 2023-05-11 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sala",
            fields=[
                (
                    "nombre_sala",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("tiempo_respuesta", models.IntegerField(default=15)),
                ("n_jugadores", models.IntegerField(default=0)),
                ("password_sala", models.CharField(default="", max_length=200)),
                (
                    "tipo_partida",
                    models.CharField(
                        choices=[
                            ("Clasico", "Clasico"),
                            ("Equipo", "Equipo"),
                            ("Tematico", "Tematico"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "tipo_sala",
                    models.CharField(
                        choices=[("Publico", "Publico"), ("Privado", "Privado")],
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "Sala",
            },
        ),
        migrations.CreateModel(
            name="UsuariosSala",
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
                ("equipo", models.IntegerField(default=1)),
                (
                    "nombre_sala",
                    models.ForeignKey(
                        db_column="nombre_sala",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usuarios_sala_usuario_nombre_sala",
                        to="sala.sala",
                    ),
                ),
            ],
            options={
                "db_table": "UsuariosSala",
            },
        ),
    ]
