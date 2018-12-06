from django.db import models
from oscar.core.loading import get_class, get_model
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel, PublishingPanel, RichTextFieldPanel
from wagtail.core.models import Orderable, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.core import blocks
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from oscar.models.fields.slugfield import SlugField
from decimal import Decimal
from django import forms
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
