from django.apps import AppConfig


class PostulationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postulations'

    def ready(self):
        import postulations.signals
