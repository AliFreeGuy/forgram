from django.apps import AppConfig


class ForgramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forgram'

    def ready(self) -> None:
        from . import signals
        