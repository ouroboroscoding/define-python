# coding=utf8
"""Tree

Represents the master parent of a record, holds special data to represent
how the entire tree is stored
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-19"

# Limit exports
__all__ = ['Tree']

# Local imports
from .base import NOT_SET
from .parent import Parent
from . import constants

class Tree(Parent):
	"""Tree

	Represents the master parent of a record, holds special data to represent
	how the entire tree is stored

	Extends:
		Parent
	"""

	def __init__(self, details: dict, extend: dict = NOT_SET):
		"""Constructor

		Initialises the instance

		Arguments:
			details (dict): Definition
			extend (dict | False): Optional, a dictionary to extend the
									definition

		Raises:
			KeyError, ValueError

		Returns
			Tree
		"""

		# Generate the details
		dDetails = Parent.make_details(details, extend)

		# If details is not a dict instance
		if not isinstance(dDetails, dict):
			raise ValueError('details in must be a dict')

		# If the name is not set
		if '__name__' not in dDetails:
			raise KeyError('__name__')

		# If the name is not valid
		if not constants.standard.match(dDetails['__name__']):
			raise ValueError('__name__')

		# Call the parent constructor
		super(Tree, self).__init__(dDetails, False)

		# Store the name
		self._name = dDetails['__name__']

		# If for some reason the array flag is set
		if '__array__' in dDetails:
			raise KeyError('__array__')