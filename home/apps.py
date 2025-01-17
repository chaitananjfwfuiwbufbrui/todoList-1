from django.apps import AppConfig
from suit.config import DjangoSuitConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
