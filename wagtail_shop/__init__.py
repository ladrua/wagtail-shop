default_app_config = 'wagtail_shop.apps.ShopConfig'

from oscar import get_core_apps as oscar_get_core_apps

WAGTAIL_SHOP_CORE_APPS = [
    'oscar',
    'oscar.apps.analytics',
    'oscar.apps.checkout',
    'oscar.apps.address',
    'oscar.apps.shipping',
    'wagtail_shop.oscar_apps.partner',
    'wagtail_shop.oscar_apps.catalogue',
    'oscar.apps.catalogue.reviews',
    'oscar.apps.basket',
    'oscar.apps.payment',
    'oscar.apps.offer',
    'oscar.apps.order',
    'oscar.apps.customer',
    'oscar.apps.promotions',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    'oscar.apps.dashboard',
    'oscar.apps.dashboard.reports',
    'oscar.apps.dashboard.users',
    'oscar.apps.dashboard.orders',
    'oscar.apps.dashboard.promotions',
    'oscar.apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.partners',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',
    'oscar.apps.dashboard.shipping',
    # 3rd-party apps that oscar depends on
    'haystack',
    'treebeard',
    'sorl.thumbnail',
    'django_tables2',
    'wagtail_shop',
]

def get_core_apps(overrides=None):
    """
    Return a list of oscar's apps amended with any passed overrides
    """
    if not overrides:
        return WAGTAIL_SHOP_CORE_APPS

    # Conservative import to ensure that this file can be loaded
    # without the presence Django.
    if isinstance(overrides, str):
        raise ValueError(
            "get_core_apps expects a list or tuple of apps "
            "to override")

    def get_app_label(app_label, overrides):
        pattern = app_label.replace('wagtail_shop.oscar_apps.', '')
        pattern = pattern.replace('oscar.apps.', '')
        for override in overrides:
            if override.endswith(pattern):
                if 'dashboard' in override and 'dashboard' not in pattern:
                    continue
                return override
        return app_label

    apps = []
    for app_label in WAGTAIL_SHOP_CORE_APPS:
        apps.append(get_app_label(app_label, overrides))
    print(apps)
    return apps
