from django.db import models
from django.template.response import TemplateResponse
from wagtail.core.models import Orderable, Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from oscar.core.loading import get_class, get_model
from django.conf import settings
from django.template.response import TemplateResponse

class AbstractShopHome(RoutablePageMixin, Page):
    mode = getattr(settings, 'WAGTAIL_SHOP_OSCARMODE', False)
    apiurl = getattr(settings, 'WAGTAIL_SHOP_APIURL', '/api')
    
    def get_context(self, request):
        products = get_model('catalogue', 'Product')
        context = super().get_context(request)
        context['shopbaseurl'] = self.get_url(request)
        context['apiurl'] = self.apiurl
        context['products'] = products.objects.all()
        return context 
    
    if mode == False:

        @route(r'^basket/$')
        def basket_summary(self, request):
            return TemplateResponse(
                request,
                'wagtail_shop/shop/basket.html',
                self.get_context(request)
            )
        
        @route(r'^basket/add/(?P<pk>\d+)/$')
        def basket_add(self, request, *args, **kwargs):
            add_view = get_class('basket.views', 'BasketAddView')
            return add_view.as_view()(request, *args, **kwargs)

    class Meta:
        abstract = True
