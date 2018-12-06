default_app_config = 'wagtail_shop.apps.ShopConfig'

from oscar import get_core_apps as oscar_get_core_apps

CORE_APPS = ['django.contrib.sites', 'django.contrib.flatpages', 'wagtail.contrib.routable_page', 'widget_tweaks'] + oscar_get_core_apps(['wagtail_shop.oscar_apps.partner','wagtail_shop.oscar_apps.catalogue']) + ['wagtail_shop', 'rest_framework', 'oscarapi']


def get_core_apps():
    return CORE_APPS
