from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'wagtail_shop'

    def ready(self):
        import wagtail_shop.signals
