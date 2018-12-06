from oscar.core.loading import get_model
from oscar.apps.checkout.forms import ShippingAddressForm as CoreShippingAddressForm
Country = get_model('address', 'Country')

class ShippingAddressForm(CoreShippingAddressForm):
	def adjust_country_field(self):
		countries = Country._default_manager.filter(
			is_shipping_country=True)

		# No need to show country dropdown if there is only one option

		if len(countries) == 1:
			self.fields.pop('country', None)
			self.instance.country = countries[0]
		else:
			self.fields['country'].queryset = countries
			self.fields['country'].initial = 'GB'
			self.fields['country'].empty_label = None
