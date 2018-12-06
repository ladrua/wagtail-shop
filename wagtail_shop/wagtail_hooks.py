from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
#from .models import Product
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from django.utils.html import format_html
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from django.contrib.staticfiles.templatetags.staticfiles import static
from oscar.core.loading import get_class, get_model
from wagtail.contrib.modeladmin.views import InspectView, IndexView
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, PageAdminURLHelper
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.http import urlquote
from .product_admin import *



# Now you just need to register your customised ModelAdmin class with Wagtail
class MyCustomInspectView(InspectView):
    def get_field_display_value(self, field_name, field=None):
        """ Return a display value for a field/attribute """

        # First we check for a 'get_fieldname_display' property/method on
        # the model, and return the value of that, if present.
        val_funct = getattr(self.instance, 'get_%s_display' % field_name, None)
        if val_funct is not None:
            if callable(val_funct):
                return val_funct()
            return val_funct

        # Now let's get the attribute value from the instance itself and see if
        # we can render something useful. raises AttributeError appropriately.
        val = getattr(self.instance, field_name)
        if field_name == 'lines':
            val = val.all()
            return val
        # if field_name == 'basket':
        #     print(val)
        #     val = val.lines.all()
        #     response = ''
        #     for obj in val:
        #         if obj.product:
        #             response += (str(obj.quantity) + ' x ' + obj.product.title + ', ')
        #
        #     return response

        if isinstance(val, models.Manager):


            val = val.all()

        if isinstance(val, models.QuerySet):

            if val.exists():
                return ', '.join(['%s' % obj for obj in val])
            return self.model_admin.get_empty_value_display(field_name)

        # wagtail.images might not be installed
        try:
            from wagtail.images.models import AbstractImage
            if isinstance(val, AbstractImage):
                # Render a rendition of the image
                return self.get_image_field_display(field_name, field)
        except RuntimeError:
            pass

        # wagtail.wagtaildocuments might not be installed
        try:
            from wagtail.documents.models import AbstractDocument
            if isinstance(val, AbstractDocument):
                # Render a link to the document
                return self.get_document_field_display(field_name, field)
        except RuntimeError:
            pass

        # Resort to returning the real value or 'empty value'
        if val or val is False:
            return val
        return self.model_admin.get_empty_value_display(field_name)

# class MyCustomIndexView(IndexView):
class MyURLHelper(AdminURLHelper):
    def get_action_url_name(self, action):
        return '%s_%s_modeladmin_%s' % (self.opts.app_label, self.opts.model_name, action)

    def _get_action_url_pattern(self, action):
        if action == 'index':
            return r'^%s/%s/$' % ('shop', self.opts.model_name)
        return r'^%s/%s/%s/$' % ('shop', self.opts.model_name,
                                 action)

    def _get_object_specific_action_url_pattern(self, action):
        return r'^%s/%s/%s/(?P<instance_pk>[-\w]+)/$' % ('shop', self.opts.model_name, action)

class MyPageURLHelper(PageAdminURLHelper):

    def get_action_url_name(self, action):
        return '%s_%s_modeladmin_%s' % (self.opts.app_label, self.opts.model_name, action)

    def _get_action_url_pattern(self, action):
        if action == 'index':
            return r'^%s/%s/$' % ('shop', self.opts.model_name)
        return r'^%s/%s/%s/$' % ('shop', self.opts.model_name,
                                 action)

    def _get_object_specific_action_url_pattern(self, action):
        return r'^%s/%s/%s/(?P<instance_pk>[-\w]+)/$' % ('shop', self.opts.model_name, action)

    def get_action_url(self, action, *args, **kwargs):
        if action in ('add', 'edit', 'delete', 'unpublish', 'copy'):
            url_name = 'wagtailadmin_pages:%s' % action
            target_url = reverse(url_name, args=args, kwargs=kwargs)
            return '%s?next=%s' % (target_url, urlquote(self.index_url))
        return super().get_action_url(action, *args, **kwargs)



class OrderModelAdmin(ModelAdmin):
    Orders = get_model('order', 'Order')
    model = Orders
    menu_label = 'Orders'  # ditch this to use verbose_name_plural from model
    menu_icon = 'doc-full-inverse'  # change as required
    list_display = ('number', 'customer', 'num_items', 'total_incl_tax', 'date_placed', 'status')
    list_filter = ('status',)
    search_fields = ('number','user__first_name','user__last_name', 'user__email')
    inspect_view_enabled=True
    inspect_view_class = MyCustomInspectView
    # inspect_view_fields_exclude = ('id','site','billing_address', 'shipping_excl_tax', 'shipping_incl_tax', 'shipping_code')
    inspect_view_fields = ( 'number', 'date_placed', 'status', 'user', 'shipping_address', 'lines', 'currency', 'total_incl_tax', 'total_excl_tax', 'shipping_method',  'guest_email')
    form_fields_exclude = ('basket','site','number', 'user', 'billing_address', 'currency', 'total_incl_tax', 'total_excl_tax', 'shipping_excl_tax', 'shipping_incl_tax', 'shipping_code', 'shipping_method', 'guest_email', 'date_placed', 'shipping_address')
    index_template_name = 'wagtail_shop/admin/order/list.html'
    inspect_template_name = 'wagtail_shop/admin/order/inspect.html'
    inspect_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    inspect_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    url_helper_class = MyURLHelper

    def customer(self, obj):
        return obj.user.get_full_name()

class CategoryModelAdmin(ModelAdmin):
    Category = get_model('catalogue', 'category')
    model = Category
    menu_label = 'Categories'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-inverse'

    inspect_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    inspect_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    url_helper_class = MyPageURLHelper

class ProductClassModelAdmin(ModelAdmin):
    ProductClass = get_model('catalogue', 'productclass')
    model = ProductClass
    menu_label = 'Product Types'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-inverse'
    inspect_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    inspect_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    url_helper_class = MyURLHelper


class ProductAttributeModelAdmin(ModelAdmin):
    ProductAttribute = get_model('catalogue', 'productattribute')
    model = ProductAttribute
    menu_label = 'Product Attributes'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-inverse'
    inspect_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    inspect_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    url_helper_class = MyURLHelper


class PartnerModelAdmin(ModelAdmin):
    Partner = get_model('partner', 'partner')
    model = Partner
    menu_label = 'Partners'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-inverse'
    inspect_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    inspect_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    url_helper_class = MyURLHelper

class StockRecordModelAdmin(ModelAdmin):
    StockRecord = get_model('partner', 'stockrecord')
    model = StockRecord
    menu_label = 'Stock Records'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder-inverse'
    inspect_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    inspect_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    index_view_extra_css = ('wagtail_shop/css/shopadmin.css',)
    index_view_extra_js = ('wagtail_shop/js/shopadmin.js',)
    url_helper_class = MyURLHelper

class MyModelSettingsAdminGroup(ModelAdminGroup):
    menu_label = 'Settings'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ProductClassModelAdmin)

class MyModelAdminGroup(ModelAdminGroup):
    menu_label = 'Shop'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ProductModelAdmin, CategoryModelAdmin, OrderModelAdmin, ProductClassModelAdmin, PartnerModelAdmin, StockRecordModelAdmin)

modeladmin_register(MyModelAdminGroup)
