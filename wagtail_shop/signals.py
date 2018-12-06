from oscar.apps.order.signals import order_placed
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

@receiver(order_placed)
def notifyshopadmin(sender, **kwargs):
    body = 'Hello, Ordernr: <a href="http://%s/admin/shop/order/inspect/%s/">#%s</a> just came in. \n Total: %s' % ('domain.com', kwargs['order'].id, kwargs['order'].number, kwargs['order'].total_incl_tax)
    email = EmailMessage(
        'New order',
        body,
        getattr(settings, "DEFAULT_FROM_EMAIL", None),
        getattr(settings, "NOTIFYEMAILS", None),
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
