from oscar.apps.basket.views import *
from django.views.generic import FormView, View
from json.encoder import py_encode_basestring_ascii

class EditBasketLineView(FormView):
    line_attribute_model = get_model('basket', 'lineattribute')

    http_method_names = ['post']

    def post(self, request):
        response = redirect('basket:summary')
        line_id = request.POST.get('line_id', '')
        attribute_id = request.POST.get('attribute_id', '')
        value = request.POST.get('value', '')
        # value = py_encode_basestring_ascii(value)[1:-1]
        value = str(value)
        attribute = self.line_attribute_model.objects.filter(id=attribute_id).get()
        attribute.value = value
        attribute.save()
        return response


class LineRemoveView(View):
    line_model = get_model('basket', 'line')

    http_method_names = ['post']

    def post(self, request):
        response = redirect('basket:summary')
        line_id = request.POST.get('line_id', '')
        self.line_model.objects.filter(id=line_id).delete()
        return response
