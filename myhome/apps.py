from django.apps import AppConfig


class MyhomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myhome'

class MyHomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myhome'

    def ready(self):
        import myhome.signals