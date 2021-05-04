from django.apps import AppConfig


class CbvaccountsConfig(AppConfig):
    name = 'cbvaccounts'

    def ready(self):
        import cbvaccounts.signals