from django.apps import AppConfig


class TrivialApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trivial_api"

    # Enviar uan señal de postmigrate para poblar al inicio
    def ready(self):
        import trivial_api.signals