from django.apps import AppConfig


class ServiceProviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'

    # def ready(self) -> None:
    #     import services.signals.signals
