from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
#from .models import Product
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from django.utils.html import format_html
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from django.contrib.staticfiles.templatetags.staticfiles import static
from oscar.core.loading import get_class, get_model
from wagtail.contrib.modeladmin.views import InspectView, IndexView, CreateView, EditView
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, PageAdminURLHelper
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.http import urlquote
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from wagtail.admin.forms import WagtailAdminModelForm
from django import forms
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.utils.text import capfirst

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks

ProductAttributeValueModel = get_model('catalogue', 'productattributevalue')
ProductModel = get_model('catalogue', 'product')
class BaseChildrenFormset(BaseInlineFormSet):
    pass

class MyCustomIndexView(IndexView):

    def product_types(self):
        ProductClass = get_model('catalogue', 'productclass')
        producttypes = ProductClass.objects.all()
        return producttypes

class MyCustomCreateView(CreateView):

    def get_product_class(self):
        ProductClass = get_model('catalogue', 'productclass')
        product_class_id = self.request.GET.get('product_type', '')
        instance = ProductClass.objects.filter(pk=product_class_id).first()
        self.product_class = instance
        return instance

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_instance()
        instance.product_class = self.get_product_class()
        kwargs.update({
            #'initial': { 'product_class': self.get_product_class()},
            'instance': instance
        })
        return kwargs

    def get_product_class(self):
        ProductClass = get_model('catalogue', 'productclass')
        product_class_id = self.request.GET.get('product_type')
        if not product_class_id:
            product_class_id = self.request.POST.get('product_type')

        product_class = ProductClass.objects.filter(pk=product_class_id).first()
        return product_class

    def get_edit_handler(self):
        original_edit_handler = self.model.edit_handler
        product_class = self.get_product_class()
        
        # if product_class and product_class.name == 'Guitar':
        #     attributes_panels = [ StreamFieldPanel('guitar_attributes') ]
        # else:
        #     attributes_panels = self.model.attributes_panels

        attributes_panels = self.model.attributes_panels
        
        edit_handler = TabbedInterface([
            ObjectList(self.model.general_panels, heading='General'),
            ObjectList(attributes_panels, heading='Attributes'),
            ObjectList(self.model.images_panels, heading='Images'),
            ObjectList(self.model.categories_panels, heading='Categories'),
            ObjectList(self.model.settings_panels, heading='Settings'),
        ])
        return edit_handler.bind_to_model(self.model)

    def get_page_subtitle(self):
        base_title = capfirst(self.verbose_name)
        title = self.get_product_class().name + ' ' + base_title 
        return title

class MyCustomEditView(EditView):

    def get_page_subtitle(self):
        base_title = self.instance.title
        title = base_title + ' - ' + self.instance.product_class.name
        return title
    
    def get_edit_handler(self):
        original_edit_handler = self.model.edit_handler
        
        # if self.instance.product_class and self.instance.product_class.name == 'Guitar':
        #     attributes_panels = [ StreamFieldPanel('guitar_attributes') ]
        # else:
        #     attributes_panels = self.model.attributes_panels

        attributes_panels = self.model.attributes_panels    
        edit_handler = TabbedInterface([
            ObjectList(self.model.general_panels, heading='General'),
            ObjectList(attributes_panels, heading='Attributes'),
            ObjectList(self.model.images_panels, heading='Images'),
            ObjectList(self.model.categories_panels, heading='Categories'),
            ObjectList(self.model.settings_panels, heading='Settings'),
        ])
        return edit_handler.bind_to_model(self.model)

class ProductsAdminURL(AdminURLHelper):

    def get_action_url_name(self, action):
        return '%s_%s_modeladmin_%s' % (self.opts.app_label, self.opts.model_name, action)

    def _get_action_url_pattern(self, action):
        if action == 'index':
            return r'^%s/%s/$' % ('shop', self.opts.model_name)
        return r'^%s/%s/%s/$' % ('shop', self.opts.model_name,
                                 action)

    def _get_object_specific_action_url_pattern(self, action):
        return r'^%s/%s/%s/(?P<instance_pk>[-\w]+)/$' % ('shop', self.opts.model_name, action)


class ProductModelAdmin(ThumbnailMixin, ModelAdmin):
    Product = get_model('catalogue', 'product')
    model = Product
    menu_label = 'Products'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pick'  # change as required
    menu_order = 9999  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = True # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('admin_thumb', 'title', 'category', 'price', 'date_updated', 'priority', 'active')
    list_filter = ('active','categories')
    search_fields = ('title',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_template_name = 'wagtail_shop/admin/product/list.html'
    create_template_name = 'wagtail_shop/admin/product/create.html'

    # Optionally tell IndexView to add buttons to a different column (if the
    # first column contains the thumbnail, the buttons are likely better off
    # displayed elsewhere)
    list_display_add_buttons = 'title'

    """
    Set 'thumb_image_field_name' to the name of the ForeignKey field that
    links to 'wagtailimages.Image'
    """
    thumb_image_field_name = 'avatar'

    # Optionally override the filter spec used to create each thumb
    thumb_image_filter_spec = 'fill-100x100' # this is the default

    # Optionally override the 'width' attribute value added to each img tag
    thumb_image_width = 100 # this is the default

    # Optionally override the class name added to each img tag
    thumb_classname = 'admin-thumb' # this is the default

    # Optionally override the text that appears in the column header
    thumb_col_header_text = 'image' # this is the default
    url_helper_class = ProductsAdminURL

    # Optionally specify a fallback image to be used when the object doesn't
    # have an image set, or the image has been deleted. It can an image from
    # your static files folder, or an external URL.
    # thumb_default = 'http://lorempixel.com/100/100'
    index_view_class = MyCustomIndexView
    create_view_class = MyCustomCreateView
    edit_view_class = MyCustomEditView
    def category(self, obj):
        stri = ""
        for category in obj.categories.all():

            stri+=category.title
            if obj.categories.all().count() > 1:
                stri+=", "
        return stri
