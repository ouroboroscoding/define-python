# coding=utf8
"""Hash

Represents a node which is a dictionary of node type to node type
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# PIP imports
from tools import clone, combine

# Local imports
from .base import Base, NOT_SET
from .node import Node
from . import constants

class Hash(Base):
	"""Hash

	Handles objects similar to Parents except where the keys are dynamic instead
	of static

	Extends:
		Base
	"""

	def __init__(self, details: dict, extend: dict = NOT_SET):
		"""Constructor

		Initialises the instance

		Arguments:
			details (dict): Definition
			extend (dict | False): Optional, a dictionary to merge with extended definitions

		Returns
			Array
		"""

		# If details is not a dict instance
		if not isinstance(details, dict):
			raise ValueError('details must be a dict')

		# Init the details
		dDetails: dict = None

		# If we have no extend at all
		if extend is NOT_SET:

			# Make a copy of the details so we don't screw up the original
			#	object
			dDetails = clone(details)

		# Else, we have an extend value
		else:

			# If it's a dictionary
			if isinstance(extend, dict):

				# Store the details by making a new object from the details and
				#	the extend
				dDetails = combine(details, extend)

			# Else, if it's false
			elif extend == False:

				# Just use the details as is, don't copy it
				dDetails = details

			# Else, we got some sort of invalid value for extend
			else:
				raise ValueError('extend must be a dict or False')

		# If the hash config is not found
		if '__hash__' not in dDetails:
			raise KeyError('__hash__')

		# If the value is not a dict
		if not isinstance(dDetails['__hash__'], dict):
			dDetails['__hash__'] = {
				'type': (dDetails['__hash__'] is True) and \
					'string' or \
					dDetails['__hash__']
			}

		# Store the key using the hash value
		self._key = Node(dDetails['__hash__'])

		# Remove it from details
		del dDetails['__hash__']

		# Call the parent constructor
		super(Hash, self).__init__(dDetails)

		# Store the child
		self._node = Base.create(dDetails)

	def child(self):
		"""Child

		Returns the child node associated with the hash

		Returns:
			Base
		"""
		return self._node

	def clean(self, value: dict | None, level: list = NOT_SET):
		"""Clean

		Makes sure both the key and value are properly stored in their correct
		representation

		Arguments:
			value (any): The value to clean

		Raises:
			ValueError

		Returns:
			any | None
		"""

		# If the level is not set
		if level is NOT_SET:
			level = []

		# If the value is None
		if value is None:

			# If it's optional, return as is
			if self._optional:
				return None

			# Missing value
			raise ValueError([['.'.join(level), 'missing']])

		# If the value is not a dict
		if not isinstance(value, dict):
			raise ValueError([['.'.join(level), 'not a valid object']])

		# Go through each key
		lErrors: list = []
		dRet: dict = {}
		for k,v in value.items():

			# Add the key to the level
			lLevel = level[:]
			lLevel.append(k)

			# Try to clean the values
			try:
				dRet[str(self._key.clean(k))] = self._node.clean(v, lLevel)
			except ValueError as e:
				lErrors.extend(e.args[0])

		# If there's errors
		if lErrors:
			raise lErrors

		# Return the cleaned value
		return dRet

	def to_dict(self):
		"""To Dict

		Returns the Hash as a dictionary in the same format as is used in
		constructing it

		Returns:
			dict
		"""

		# Init the dictionary we will return
		dRet: dict = {}

		# Add the hash key
		dRet['__hash__'] = self._key.to_dict()

		# Add the child type
		dRet['__type__'] = self._node.to_dict()

		# Get the parents dict and add it to the return
		dRet.update(super(Hash, self).to_dict())

		# Return
		return dRet

	def valid(self, value: dict | None, level: list = NOT_SET):
		"""Valid

		Checks if a value is valid based on the instance's values. If any errors
		occur, they can be found in [instance].validation_failures as a list

		Arguments:
			value (dict | None): The value to validate

		Returns:
			bool
		"""

		# If the level is not set
		if level is NOT_SET:
			level = []

		# Reset validation failures
		self._validation_failures = []

		# If the value is None
		if value is None:

			# If it's optional, we're good
			if self._optional:
				return True

			# Invalid value
			self._validation_failures.append(('.'.join(level), 'missing'))

		# If the value isn't a dictionary
		if not isinstance(value, dict):
			self._validation_failures.append(('.'.join(level), 'not a valid object'))
			return False

		# Init the return, assume valid
		bRet = True

		# Go through each key and value
		for k,v in value.items():

			# Add the field to the level
			lLevel = level[:]
			lLevel.append(k)

			# If the key isn't valid
			if not self._key.valid(k):
				self._validation_failures.append(('.'.join(lLevel), 'invalid key: %s' % str(k)))
				bRet = False
				continue

			# Check the value
			if not self._node.valid(v, lLevel):
				self._validation_failures.extend(self._node.validation_failures)
				bRet = False
				continue

		# Return whatever the result was
		return bRet

# Register with Base
Base.register('hash', Hash)