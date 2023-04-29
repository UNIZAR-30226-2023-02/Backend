# Generated by Django 4.1.7 on 2023-04-29 10:13

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        default="ad", max_length=50, primary_key=True, serialize=False
                    ),
                ),
                (
                    "correo",
                    models.EmailField(
                        default="example@gmail.com", max_length=254, unique=True
                    ),
                ),
                ("telefono", models.IntegerField(default=0)),
                ("fecha_nac", models.DateField(default="1997-10-19")),
                ("password", models.CharField(default="", max_length=200)),
                ("monedas", models.IntegerField(default=0)),
                (
                    "image_perfil",
                    models.CharField(
                        default="/static/images/perfil/default_perfil.png",
                        max_length=200,
                    ),
                ),
                (
                    "image_tablero",
                    models.CharField(
                        default="/static/images/perfil/default_tablero.png",
                        max_length=200,
                    ),
                ),
                (
                    "image_ficha",
                    models.CharField(
                        default="/static/images/perfil/default_ficha.png",
                        max_length=200,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "db_table": "Usuario",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Objetos",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("coste", models.IntegerField(default=5)),
                (
                    "tipo",
                    models.CharField(
                        choices=[("ficha", "Ficha"), ("tablero", "Tablero")],
                        max_length=7,
                    ),
                ),
                ("image", models.CharField(max_length=200)),
            ],
            options={
                "db_table": "Objetos",
            },
        ),
        migrations.CreateModel(
            name="Estadisticas",
            fields=[
                (
                    "username",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="estadisticas_username",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("geografia_bien", models.IntegerField(default=0)),
                ("geografia_mal", models.IntegerField(default=0)),
                ("arte_y_literatura_bien", models.IntegerField(default=0)),
                ("arte_y_literatura_mal", models.IntegerField(default=0)),
                ("historia_bien", models.IntegerField(default=0)),
                ("historia_mal", models.IntegerField(default=0)),
                ("entretenimiento_bien", models.IntegerField(default=0)),
                ("entretenimiento_mal", models.IntegerField(default=0)),
                ("ciencias_bien", models.IntegerField(default=0)),
                ("ciencias_mal", models.IntegerField(default=0)),
                ("deportes_bien", models.IntegerField(default=0)),
                ("deportes_mal", models.IntegerField(default=0)),
                ("quesitos", models.IntegerField(default=0)),
                ("partidas_ganadas", models.IntegerField(default=0)),
                ("partidas_perdidas", models.IntegerField(default=0)),
            ],
            options={
                "db_table": "Estadisticas",
            },
        ),
        migrations.CreateModel(
            name="Tiene",
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
                ("enUso", models.IntegerField(default=0)),
                (
                    "id_objeto",
                    models.ForeignKey(
                        db_column="id_objeto",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="id_objeto",
                        to="trivial_api.objetos",
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="username_objeto",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "Tiene",
            },
        ),
        migrations.CreateModel(
            name="Amigos",
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
                    "user1",
                    models.ForeignKey(
                        db_column="user1",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user1",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user2",
                    models.ForeignKey(
                        db_column="user2",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user2",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "Amigos",
            },
        ),
        migrations.AddConstraint(
            model_name="tiene",
            constraint=models.UniqueConstraint(
                fields=("id_objeto", "username"), name="usuario_objeto_pk"
            ),
        ),
        migrations.AddConstraint(
            model_name="amigos",
            constraint=models.UniqueConstraint(
                fields=("user1", "user2"), name="usuario_amigo_pk"
            ),
        ),
    ]
