from django.db import models  # noqa isort:skip
from oscar.apps.basket.abstract_models import AbstractBasket
import datetime

class Basket(AbstractBasket):

	def _create_line_reference(self, product, stockrecord, options):
		"""
		Returns a reference string for a line based on the item
		and its options.
		"""
		ts = datetime.datetime.now().timestamp()
		base = '%s_%s_%s' % (product.id, stockrecord.id, ts)
		return base
		if not options:
			return base
		repr_options = [{'option': repr(option['option']),
						 'value': repr(option['value'])} for option in options]
		return "%s_%s" % (base, zlib.crc32(repr(repr_options).encode('utf8')))

from oscar.apps.basket.models import *
