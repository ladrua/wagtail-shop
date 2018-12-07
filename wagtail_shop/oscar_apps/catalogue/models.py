from wagtail_shop.oscar_apps.catalogue.abstract_models import *

class Category(AbstractCategory):
    pass

class ProductClass(AbstractProductClass):
    pass

class ProductCategory(AbstractProductCategory):
    pass

class Product(AbstractProduct):
    pass

class Image(AbstractImage):
    pass

class ProductImage(AbstractProductImage, Image):
    pass

from oscar.apps.catalogue.models import *  # noqa isort:skip
