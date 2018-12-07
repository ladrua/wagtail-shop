from django.db import models
from django.conf import settings
from oscar.core.loading import get_class, get_model
from oscar.apps.catalogue.abstract_models import AbstractProductCategory, AbstractProductAttributeValue
from oscar.apps.catalogue.abstract_models import AbstractProduct as OscarAbstractProduct
from oscar.apps.catalogue.abstract_models import AbstractProductClass as OscarAbstractProductClass
from oscar.apps.catalogue.abstract_models import AbstractProductImage as OscarAbstractProductImage
from oscar.apps.catalogue.abstract_models import AbstractProductCategory as OscarAbstractProductCategory
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

# from oscar.apps.catalogue.models import ProductClass
Selector = get_class('partner.strategy', 'Selector')
Partner = get_model('partner', 'partner')
StockRecord = get_model('partner', 'stockrecord')

class AbstractCategory(Page):
    """
    The Oscars Category as a Wagtail Page
    This works because they both use Treebeard
    """
    template = "catalogue/category.html"
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
        ImageChooserPanel('image'),
    ]
    settings_panels = Page.settings_panels
    
    parent_page_types = ['wagtail_shop.ShopHome', 'Category']
    subpage_types = ['Category']
    @classmethod
    def add_root(cls, **kwargs):
        """
        Adds a Catalogue page node to Wagtail's tree root node. Note that this
        isn't at depth=1 as that's Wagtail's root.
        """
        node = Category.objects.filter(depth=1).first()
        return node.add_child(**kwargs)

    @classmethod
    def get_root_nodes(cls):
        """
        :returns: A queryset containing the root nodes in the tree. This
        differs from the default implementation to find category page root
        nodes by `content_type`.
        """
        content_type = ContentType.objects.get_for_model(cls)
        depth = (cls.objects.filter(content_type=content_type).aggregate(
            depth=models.Min('depth')))['depth']

        if depth is not None:
            return cls.objects.filter(content_type=content_type, depth=depth)

        return cls.objects.filter(content_type=content_type)

    def generate_slug(self):
        """
        Generates a slug for a category. This makes no attempt at generating
        a unique slug.
        """
        return slugify(self.name)

    def get_ancestors_and_self(self):
        return list(self.get_ancestors()) + [self]

    def get_categories(self):
        """
        Return a list of the current category and its ancestors
        """
        return list(self.get_descendants()) + [self]

    @classmethod
    def get_tree(cls, parent=None):
        return cls.objects.all()

    def get_absolute_url(self):
        return self.url

    @staticmethod
    def get_search_handler(*args, **kwargs):
        from oscar.apps.catalogue.search_handlers import (
            get_product_search_handler_class
        )
        return get_product_search_handler_class()(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        self.search_handler = self.get_search_handler(
            request.GET, request.get_full_path(), self.get_categories())
        context = super(AbstractCategory, self).get_context(request, *args, **kwargs)
        context['category'] = self
        search_context = self.search_handler.get_search_context_data(
            'products'
        )
        context.update(search_context)
        return context

    def ensure_slug_uniqueness(self):
        """
        Ensures that the category's slug is unique amongst it's siblings.
        This is inefficient and probably not thread-safe.
        """
        unique_slug = self.slug
        siblings = self.get_siblings().exclude(pk=self.pk)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        """
        Oscar traditionally auto-generated slugs from names. As that is
        often convenient, we still do so if `slug` is not supplied through
        other means. Also, Wagtail's Page requires `title` where Oscar requires
        `name`. Therefore we set `title` as `name` if `name` but no `title`
         supplied, else set `name` as `title`.
        """

        # Set title and name
        if self.name and not self.title:
            self.title = self.name
        else:
            self.name = self.title

        # Set slug if not supplied
        if self.slug:
            super(AbstractCategory, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            super(AbstractCategory, self).save(*args, **kwargs)
            # We auto-generated a slug, so we need to make sure that it's
            # unique. As we need to be able to inspect the category's siblings
            # for that, we need to wait until the instance is saved. We
            # update the slug and save again if necessary.
            self.ensure_slug_uniqueness()

    class Meta:
        abstract = True
        verbose_name_plural = "Categories"

class AbstractProductClass(OscarAbstractProductClass):
    class Meta:
        abstract = True
        verbose_name = "Product Type"

class AbstractProduct(ClusterableModel, OscarAbstractProduct):
    priority = models.IntegerField(default='0')
    active = models.BooleanField(default=True)
    description = RichTextField(blank=True)
    price = models.DecimalField(default=None, max_digits=18, decimal_places=2, blank=True, help_text="Price including VAT")
    sku = models.CharField(max_length = 255, blank=True )
    default_attributes = StreamField([
        ('attribute', blocks.StructBlock([
            ('key', blocks.CharBlock()),
            ('value', blocks.CharBlock()),
        ], icon='table'))
    ], blank=True)

    product_class = models.ForeignKey(
        'catalogue.ProductClass',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Product type'), related_name="products",
        help_text=_("Choose what type of product this is"),
        default=1)
    general_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('description', classname="full"),
        FieldPanel('price', classname="full"),
    ]
    images_panels = [
        MultiFieldPanel(
            [
                InlinePanel('images', label="Image"),                
            ],
            heading="Images",
            classname=None
        )
    ]

    attributes_panels = [
        StreamFieldPanel('default_attributes'),
    ]

    categories_panels = [
        MultiFieldPanel(
            [
                InlinePanel('product_category', label="Category"),
            ],
            heading="Categories",
            classname=None
        )
    ]

    settings_panels = [
        FieldPanel('active'),
        FieldPanel('sku'),
        FieldPanel('priority'),
        FieldPanel('product_class'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(attributes_panels, heading='Attributes'),
        ObjectList(images_panels, heading='Images'),
        ObjectList(categories_panels, heading='Categories'),
        ObjectList(settings_panels, heading='Settings'),
    ])

    # base_form_class = ProductForm
    @property
    def get_absolute_url(self):
        return ""
    
    def avatar_property(self):
        return self.images.first().image
    avatar_property.short_description = "Full name of the person"
    avatar = property(avatar_property)

    def primary_image(self):
        if self.images.first():

            image = self.images.first().image

            return image
        else:
            return None

    def save(self, *args, **kwargs):

        if not self.pk:
            super().save(*args, **kwargs)
            if not self.sku :
                self.sku = self.pk
            partner = Partner.objects.first()
            exc_vat = Decimal(self.price)/(Decimal('1') + Decimal(str(Selector.strategy(self).rate)))
            stock = StockRecord(partner=partner, product=self, partner_sku=self.sku, price_excl_tax=exc_vat)
            stock.save()


        else:
            stockrecord = self.stockrecords.first()
            exc_vat = Decimal(self.price)/(Decimal('1') + Decimal(str(Selector.strategy(self).rate)))
            stockrecord.price_excl_tax=exc_vat
            if not self.sku or self.sku == '':
                self.sku = self.pk
            stockrecord.partner_sku=self.sku
            stockrecord.save()


        super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        abstract = True
        app_label = 'catalogue'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ["-active", "-priority", "-date_created"]


class AbstractImage(models.Model):
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)
    caption = models.TextField("Caption", blank=True)
    original = models.ImageField("Original", upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255)

    panels = [
    FieldRowPanel([
    ImageChooserPanel('image', classname="col12"),
    FieldPanel('caption', classname="col12"),
        ], classname='')
    ]
    
    # @property
    # def original(self):
    #     return image.original
    
    class Meta:
        abstract = True
        verbose_name = "Hello"
        
class AbstractProductImage(Orderable):
    product = ParentalKey('catalogue.Product', related_name='images', on_delete=models.CASCADE, blank=False,)

    class Meta:
        abstract = True

class AbstractProductCategory(Orderable, OscarAbstractProductCategory):
    product = ParentalKey('catalogue.Product', on_delete=models.CASCADE, verbose_name=_("Product"), related_name='product_category')

    class Meta:
        abstract = True
        unique_together = ('product', 'category')
