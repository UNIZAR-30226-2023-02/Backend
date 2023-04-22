# Generated by Django 4.1.7 on 2023-04-22 12:56

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
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="static/images/perfil/"
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
            name="Casilla_Tematica",
            fields=[
                ("casilla", models.IntegerField(primary_key=True, serialize=False)),
                ("tematica", models.CharField(max_length=50)),
                ("quesito", models.BooleanField()),
            ],
            options={
                "db_table": "Casilla_Tematica",
            },
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
                ("image", models.ImageField(upload_to="static/images/objetos/")),
            ],
            options={
                "db_table": "Objetos",
            },
        ),
        migrations.CreateModel(
            name="Partida",
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
                ("tipo", models.CharField(max_length=50)),
                ("terminada", models.BooleanField(default=False)),
                ("orden_jugadores", models.CharField(max_length=100)),
                ("turno_actual", models.IntegerField(default=0)),
            ],
            options={
                "db_table": "Partida",
            },
        ),
        migrations.CreateModel(
            name="Pregunta",
            fields=[
                (
                    "enunciado",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("r1", models.CharField(blank=True, max_length=200)),
                ("r2", models.CharField(blank=True, max_length=200)),
                ("r3", models.CharField(blank=True, max_length=200)),
                ("r4", models.CharField(blank=True, max_length=200)),
                ("rc", models.IntegerField()),
                ("categoria", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "Pregunta",
            },
        ),
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
                (
                    "creador_username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creador_sala",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "Sala",
            },
        ),
        migrations.CreateModel(
            name="Estadisticas",
            fields=[
                (
                    "user_id",
                    models.OneToOneField(
                        db_column="user_id",
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
                        to="trivial_api.sala",
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usuarios_sala_usuario",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "UsuariosSala",
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
            name="Tablero",
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
                ("tirada_dado", models.IntegerField()),
                (
                    "casilla_actual",
                    models.ForeignKey(
                        db_column="casilla_actual",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tablero_ac",
                        to="trivial_api.casilla_tematica",
                    ),
                ),
                (
                    "casilla_nueva",
                    models.ForeignKey(
                        db_column="casilla_nueva",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tablero_nu",
                        to="trivial_api.casilla_tematica",
                    ),
                ),
            ],
            options={
                "db_table": "Tablero",
            },
        ),
        migrations.CreateModel(
            name="Juega",
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
                ("posicion", models.IntegerField(default=72)),
                ("q_historia", models.BooleanField(default=False)),
                ("q_arte", models.BooleanField(default=False)),
                ("q_deporte", models.BooleanField(default=False)),
                ("q_ciencia", models.BooleanField(default=False)),
                ("q_entretenimiento", models.BooleanField(default=False)),
                ("q_geografia", models.BooleanField(default=False)),
                (
                    "id_jugador",
                    models.ForeignKey(
                        db_column="id_jugador",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="id_jugador",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "id_partida",
                    models.ForeignKey(
                        db_column="id_partida",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="id_partida",
                        to="trivial_api.partida",
                    ),
                ),
            ],
            options={
                "db_table": "Juega",
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
            model_name="usuariossala",
            constraint=models.UniqueConstraint(
                fields=("nombre_sala", "username"), name="usuario_sala_pk"
            ),
        ),
        migrations.AddConstraint(
            model_name="tiene",
            constraint=models.UniqueConstraint(
                fields=("id_objeto", "username"), name="usuario_objeto_pk"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="tablero",
            unique_together={("casilla_actual", "casilla_nueva")},
        ),
        migrations.AddConstraint(
            model_name="juega",
            constraint=models.UniqueConstraint(
                fields=("id_jugador", "id_partida"), name="usuario_partida_pk"
            ),
        ),
        migrations.AddConstraint(
            model_name="amigos",
            constraint=models.UniqueConstraint(
                fields=("user1", "user2"), name="usuario_amigo_pk"
            ),
        ),
    ]
