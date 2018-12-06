from django.shortcuts import render, redirect
import logging
# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render
from oscar.core.loading import get_class, get_model
from oscar.apps.checkout import mixins
from wagtail.admin.decorators import require_admin_access
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
logger = logging.getLogger('oscar.checkout')


@require_admin_access
def changeorderstatus(request, pk, status):
    Order = get_model('order', 'order')
    instance = Order.objects.filter(pk=pk).first()
    try:
        fromstatus = instance.status
        instance.set_status(status)
        messages.add_message(request, messages.SUCCESS, 'Changed status from %s to %s.' % (fromstatus, status))
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Something failed %s' % e)

    return redirect('/admin/shop/order/inspect/%s/' % pk)


@require_admin_access
def resendorderconfirmation(request, pk, email=None, **kwargs):
    Order = get_model('order', 'order')
    CommunicationEventType = get_model('customer', 'CommunicationEventType')
    Dispatcher = get_class('customer.utils', 'Dispatcher')
    instance = Order.objects.filter(pk=pk).first()
    ctx = {
        'user': request.user,
        'order': instance,
        'site': get_current_site(request),
        'lines': instance.lines.all()
    }
    code = 'ORDER_PLACED'
    event_type = None
    message = CommunicationEventType.objects.get_and_render(code, ctx)
    logger.info("Order #%s - sending %s messages", instance.number, code)
    dispatcher = Dispatcher(logger)
    try:

        email_address = request.POST.get('email')
        # dispatcher.dispatch_order_messages(instance, message, event_type, email_address)
        dispatched_messages = dispatcher.dispatch_anonymous_messages(email_address, message)
        dispatcher.create_communication_event(instance, event_type, dispatched_messages)
        messages.add_message(request, messages.SUCCESS, 'Resent Order Confirmation to %s' % email_address)
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Something failed %s' % e)
    return HttpResponse('/admin/shop/order/inspect/%s/' % pk)
