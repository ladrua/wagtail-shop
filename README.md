Wagtail Shop
=====

Simple shop based on django-oscar.


Quick start
-----------

1. `pip install wagtail-shop`

2. Add `from oscar.defaults import *` to your settings.py file.

3. Import and append `get_core_apps()` to your INSTALLED_APPS, and add required packages like this:
```
    from wagtail_shop import get_core_apps

    INSTALLED_APPS = [
        ...
	'django.contrib.sites',
	'django.contrib.flatpages',
	'wagtail.contrib.routable_page',
	'wagtail.contrib.modeladmin',
	'widget_tweaks',
    ] + get_core_apps()
```
4. Add `oscar.apps.basket.middleware.BasketMiddleware` to your MIDDLEWARE
   
5. Run migrations `./manage.py migrate`

6. Before you can add any products you must create at least one `Product Type` and add one `Partner` in the Wagtail admin interface.
