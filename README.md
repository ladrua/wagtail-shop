Wagtail Shop
=====

Using Wagtail as admin for [django-oscar](https://github.com/django-oscar/django-oscar).

**NB: This is currently in beta**

The overal goal of this project is to be able to administer all aspects of django-oscar from the wagtail admin.

Status
------
Features:

* Add/Edit Products.
* Add/Edit Categories.
* View Orders.
* Add/Edit Product Classes.
* Add/Edit Partners.
* Add/Edit StockRecords.


Todo:

* Manage Customers.
* Better handling of StockRecords.
* Add a `ProductChooser` to use in Pages.

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

What's next?
------------

You should now be able to follow the [django-oscar documentation](https://django-oscar.readthedocs.io) for further details. 
There are a few exceptions:

1. Instead of using `./manage.py oscar_fork_app` when forking an app, use `./manage.py wagtail_shop_fork_app`.

2. If setting up with the default templates provided with django-oscar, the images won't work, and you would have to update the image tags in the template to use [Wagtails image tags](https://docs.wagtail.io/en/latest/topics/images.html) 

Screenshots
-----------
![Product detail](/screenshots/product-list.png?raw=true "Product list")

![Product detail](/screenshots/product-detail.png?raw=true "Product detail")
