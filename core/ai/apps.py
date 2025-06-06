from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.ai'


    def ready(self):

        from . import services

        services.get_all_chats()