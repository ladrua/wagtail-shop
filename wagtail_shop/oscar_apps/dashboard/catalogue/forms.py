from django import forms
from oscar.core.loading import get_model
from oscar.apps.dashboard.catalogue.forms import *
Product = get_model('catalogue', 'Product')
class ProductForm(ProductForm):


    class Meta:
        model = Product
        fields = [
            'title', 'upc', 'description', 'is_discountable', 'structure', 'priority']
        widgets = {
            'structure': forms.HiddenInput()
        }
