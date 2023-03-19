# coding=utf8
"""Array

Represents a node which is a list of multiple nodes
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# PIP imports
from tools import clone, combine

# Local imports
from .base import Base
from . import constants

class Array(Base):
	"""Array

	Handles lists of nodes

	Extends:
		Base
	"""

	_VALID_ARRAY = ['unique', 'duplicates']
	"""Valid Array

	Holds a list of valid values used to represent arrays types"""

	def __init__(self, details: dict, extend: dict = None):
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
		if extend is None:

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

		# If the array config is not found
		if '__array__' not in dDetails:
			raise KeyError('__array__')

		# If the value is not a dict
		if not isinstance(dDetails['__array__'], dict):
			dDetails['__array__'] = {
				'type': dDetails['__array__']
			}

		# If the type is missing
		if not 'type' in dDetails['__array__']:
			self._type = 'unique'

		# Or if the type is invalid
		elif dDetails['__array__']['type'] not in self._VALID_ARRAY:
			raise ValueError('"%s" is not a valid type for __array__' %
								str(dDetails['__array__']['type']))

		# Else, store it
		else:
			self._type = dDetails['__array__']['type']

		# Call the Base constructor
		super(Array, self).__init__(dDetails)

		# Init the min/max values
		self._minimum = None
		self._maximum = None

		# If there's a minimum or maximum present
		if 'minimum' in dDetails['__array__'] \
			or 'maximum' in dDetails['__array__']:
			self.minmax(
				('minimum' in dDetails['__array__'] and dDetails['__array__']['minimum'] or None),
				('maximum' in dDetails['__array__'] and dDetails['__array__']['maximum'] or None)
			)

		# Remove the __array__ field from details
		del dDetails['__array__']

		# Create the child node
		self._node = Base.create(dDetails)

	def child(self):
		"""Child

		Returns the child node associated with the array

		Returns:
			Base
		"""
		return self._node

	def clean(self, value: list | None, level: list = []):
		"""Clean

		Goes through each of the values in the list, cleans it, stores it, and
		returns a new list

		Arguments:
			value (list | None): The value to clean

		Returns:
			list | None
		"""

		# If the value is None and it's optional, return as is
		if value is None:

			# If it's optional
			if self._optional:
				return None

			# Else, it's a missing value
			raise ValueError([['.'.join(level), 'missing']])

		# If the value is not a list
		if not isinstance(value, list):
			raise ValueError([['.'.join(level), 'not an array']])

		# Go through each value
		lErrors: list = []
		lRet: list = []
		for i in range(len(value)):

			# Add the field to the level
			lLevel = level[:]
			lLevel.append('[%d]' % i)

			# Try to clean it
			try:
				lRet.append(self._node.clean(value[i], lLevel))
			except ValueError as e:
				lErrors.extend(e.args[0])

		# If there's any errors
		if lErrors:
			raise lErrors

		# Return the cleaned list
		return lRet

	def minmax(self, minimum: int = None, maximum: int = None):
		"""Min/Max

		Sets or gets the minimum and maximum number of items for the Array

		Arguments
			minimum (int): The minimum value
			maximum (int): The maximum value

		Raises:
			ValueError

		Returns:
			None
		"""

		# If neither minimum or maximum is set, this is a getter
		if minimum is None and maximum is None:
			return {
				'minimum': self._minimum,
				'maximum': self._maximum
			}

		# If the minimum is set
		if minimum is not None:

			# If it's a string
			if isinstance(minimum, str):

				# If it's invalid
				if not constants.regex.int.match(minimum):
					raise ValueError('"minimum" of array must be an integer')

				# Else, convert it to a number
				minimum = int(minimum, 0)

			# Else, if it's not an int
			elif not isinstance(minimum, int):
				raise ValueError('"minimum" of array must be an integer')

			# If it's below zero
			if minimum < 0:
				raise ValueError('"minimum" of array must be an unsigned integer')

			# Store the minimum
			self._minimum = minimum

		# If the maximum is set
		if maximum is not None:

			# If it's a string
			if isinstance(maximum, str):

				# If it's invalid
				if not constants.regex.int.match(maximum):
					raise ValueError('"maximum" of array must be an integer')

				# Else, convert it to a number
				maximum = int(maximum, 0)

			# Else, if it's not an int
			elif not isinstance(maximum, int):
				raise ValueError('"maximum" of array must be an integer')

			# If it's below zero
			if maximum < 0:
				raise ValueError('"maximum" of array must be an unsigned integer')

			# If we also have a minimum and the max is somehow below it
			if self._minimum \
				and maximum < self._minimum:
				raise ValueError('"maximum" of array must not be less than "minimum"')

			# Store the maximum
			self._maximum = maximum

	def to_dict(self):
		"""To Dictionary

		Returns the Array as a dictionary in the same format as is used in
		constructing it

		Returns:
			dict
		"""

		# Init the dictionary we will return
		dRet: dict = {}

		# If either a min or a max is set
		if self._minimum or self._maximum:

			# Set the array element as it's own dict
			dRet['__array__'] = {
				'type': self._type
			}

			# If there is a minimum
			if self._minimum:
				dRet['__array__']['minimum'] = self._minimum

			# If there is a maximum
			if self._maximum:
				dRet['__array__']['maximum'] = self._maximum

		# Else, just add the type as the array element
		else:
			dRet['__array__'] = self._type

		# Add the child type
		dRet['__type__'] = self._node.to_dict()

		# Get the parents dict and add it to the return
		dRet.update(super(Array, self).to_dict())

		# Return
		return dRet

	def type(self, type: str = None):
		"""Type

		Getter/Setter for the type of array

		Returns:
			str | None
		"""

		# If a type was passed, it's a setter
		if type is not None:

			# If the value is invalid
			if type not in self._VALID_ARRAY:
				raise ValueError('"%s" is not a valid type for __array__' % str(type))

			# Store the new type
			self._type = type

		# Else, it's a getter
		else:
			return self._type

	def valid(self, value: list | None, level: list = []):
		"""Valid

		Checks if a value is valid based on the instance's values. If any errors
		occur, they can be found in [instance].validation_failures as a list

		Arguments:
			value (list): The value to validate

		Returns:
			bool
		"""

		# Reset validation failures
		self._validation_failures = []

		# If the value is None
		if value is None:

			# If it's optional, we're good
			if self._optional:
				return True

			# Invalid value
			self._validation_failures.append(('.'.join(level), 'missing'))

		# If the value isn't a list
		if not isinstance(value, list):
			self._validation_failures.append(('.'.join(level), 'not an array'))
			return False

		# Init the return, assume valid
		bRet = True

		# Keep track of duplicates
		if self._type == 'unique':
			lItems	= []

		# Go through each item in the list
		for i in range(len(value)):

			# Add the field to the level
			lLevel = level[:]
			lLevel.append('[%d]' % i)

			# If the element isn't valid, return false
			if not self._node.valid(value[i], lLevel):
				self._validation_failures.extend(self._node.validation_failures[:])
				bRet = False
				continue

			# If we need to check for duplicates
			if self._type == 'unique':

				# Try to get an existing item
				try:

					# If it is found, we have a duplicate
					iIndex = lItems.index(value[i])

					# Add the error to the list
					self._validation_failures.append(('.'.join(lLevel), 'duplicate of %s[%d]' % ('.'.join(level), iIndex)))
					bRet = False
					continue

				# If a Value Error is thrown, there is no duplicate, add the
				# 	value to the list and continue
				except ValueError:
					lItems.append(value[i])

		# If there's a minumum
		if self._minimum is not None:

			# If we don't have enough
			if len(value) < self._minimum:
				self._validation_failures.append(('.'.join(level), 'did not meet minimum'))
				bRet = False

		# If there's a maximum
		if self._maximum is not None:

			# If we have too many
			if len(value) > self._maximum:
				self._validation_failures.append(('.'.join(level), 'exceeds maximum'))
				bRet = False

		# Return whatever the result was
		return bRet

# Register with Base
Base.register('array', Array)