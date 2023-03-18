# Generated by Django 4.1.7 on 2023-03-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trivial_api", "0003_remove_usuario_correo_alter_usuario_password_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="correo",
            field=models.EmailField(
                default="example@gmail.com", max_length=254, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="password",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="username",
            field=models.CharField(default="ad", max_length=50, unique=True),
        ),
    ]
