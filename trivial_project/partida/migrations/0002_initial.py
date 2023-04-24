# Generated by Django 4.1.7 on 2023-04-24 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("partida", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="juega",
            name="username",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterUniqueTogether(
            name="tablero",
            unique_together={("casilla_actual", "casilla_nueva")},
        ),
        migrations.AddConstraint(
            model_name="juega",
            constraint=models.UniqueConstraint(
                fields=("username", "id_partida"), name="usuario_partida_pk"
            ),
        ),
    ]
