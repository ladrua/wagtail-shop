from __future__ import unicode_literals

from django.db import models

from wagtail.core.models import Orderable, Page
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel

from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.search import index
from modelcluster.models import ClusterableModel
from oscar.core.loading import get_class, get_model
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from decimal import Decimal


OscarProduct = get_model('catalogue', 'product')
ProductClass = get_model('catalogue', 'productclass')
StockRecord = get_model('partner', 'stockrecord')
Partner = get_model('partner', 'partner')
Selector = get_class('partner.strategy', 'Selector')


class Image(models.Model):
	image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)
	caption = models.TextField("Caption", blank=True)

	panels = [
    FieldRowPanel([
		ImageChooserPanel('image', classname="col12"),
		FieldPanel('caption', classname="col12"),
        ], classname='')
	]

	class Meta:
		abstract = True
		verbose_name = "Hello"


class Product(ClusterableModel):
    title = models.CharField(max_length = 255 )
    description = RichTextField(blank=True)
    includes = RichTextField(blank=True)
    price = models.DecimalField(default=None, max_digits=18, decimal_places=2, blank=True, help_text="Price including VAT")
    sku = models.CharField(max_length = 255, blank=True )
    active = models.BooleanField(default=True)
    priority = models.CharField(max_length = 255, default="0" )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def avatar_property(self):
        return self.images.first().image
    avatar_property.short_description = "Full name of the person"
    avatar = property(avatar_property)
    oscar_product = models.ForeignKey(
        OscarProduct,
        on_delete=models.CASCADE,
        related_name='wag_product',
        verbose_name="Oscar Product",
        null=True, blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('description', classname="full"),
        FieldPanel('includes', classname="full"),
        FieldPanel('price', classname="full"),
    ]
    images_panels = [
        InlinePanel('images', label="Images"),
    ]
    settings_panels = [
        FieldPanel('active'),
        FieldPanel('sku'),
        FieldPanel('priority'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(images_panels, heading='Images'),
        ObjectList(settings_panels, heading='Settings'),
    ])

    def save(self, *args, **kwargs):


        if not self.pk:

            product_class = ProductClass.objects.filter(pk=1).first()
            oprod = OscarProduct(title=self.title, structure="standalone", product_class=product_class)
            oprod.save()
            if not self.sku :
                self.sku = oprod.id
            partner = Partner.objects.filter(pk=1).first()
            exc_vat = Decimal(self.price)/(Decimal('1') + Decimal(str(Selector.strategy(self).rate)))
            stock = StockRecord(partner=partner, product=oprod, partner_sku=self.sku, price_excl_tax=exc_vat)
            stock.save()

            self.oscar_product = oprod

        else:
            self.oscar_product.title = self.title
            self.oscar_product.save()
            stockrecord = self.oscar_product.stockrecords.first()
            exc_vat = Decimal(self.price)/(Decimal('1') + Decimal(str(Selector.strategy(self).rate)))
            stockrecord.price_excl_tax=exc_vat
            stockrecord.partner_sku=self.sku
            stockrecord.save()


        super().save(*args, **kwargs)  # Call the "real" save() method.

    def delete(self, *args, **kwargs):
        print(self.oscar_product.id)
        self.oscar_product.delete()
        super(Product, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-active", "-priority"]

class Images(Orderable, Image):
	page = ParentalKey('shop.Product', related_name='images', on_delete=models.CASCADE, blank=False,)
