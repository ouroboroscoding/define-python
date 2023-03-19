# coding=utf8
"""Base

Contains the class that all other Define classes extend from
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Python imports
import abc
import copy
import sys

# PIP imports
import jsonb

# Local imports
from . import constants

class Base(abc.ABC):
	"""Base

	The class all other Define types must extend

	Extends:
		abc.ABC
	"""

	__classes = {}
	"""Class """

	def __init__(self, details: dict):
		"""Constructor (__init__)

		Creates a new instance

		Arguments:
			details (dict): The define structure
			class_name (str): The name
		"""

		# If the details are not an object
		if not isinstance(details, dict):
			raise ValueError('details must be a dict in %s.%s' % (
				self.__class__.__name__,
				sys._getframe().f_code.co_name
			))

		# Store the class name for the child
		self.__class = self.__class__.__name__

		# Init the list of the last falures generated in valid
		self._validation_failures = None

		# Init the optional flag, assume all nodes are necessary
		self._optional = False

		# If the details contains an optional flag
		if '__optional__' in details:

			# If it's a valid bool, store it
			if isinstance(details['__optional__'], bool):
				self._optional = details['__optional__']

			# Else, write a warning to stderr
			else:
				sys.stderr.write('"%s" is not a valid value for __optional__, assuming False' % str(details['__optional__']))

			# Remove it from details
			del details['__optional__']

		# Init the special dict
		self.__special = {}

		# If there are any other special fields in the details
		for k in (tuple(details.keys())):

			# If key is special
			oMatch = constants.special.key.match(k)
			if oMatch:

				# Store it with the other specials then remove it
				self.__special[oMatch.group(1)] = details[k]
				del details[k]

	def __repr__(self):
		"""Representation (__repr__)

		Returns a string representation of the instance

		Returns:
			str
		"""
		return '<%s: %s>' % (
			self.class_name(),
			str(self.to_dict())
		)

	@property
	def class_name(self):
		"""Class Name

		Returns the class of the Node instance

		Returns:
			str
		"""
		return self.__class

	@abc.abstractmethod
	def clean(self, value: any, level: list):
		"""Clean

		As validation allows for strings representing non-string values, it is
		useful to be able to "clean" a value and turn it into the value it was
		representing, making sure that data in data stores is accurate, and not
		representitive

		Arguments:
			value (any): The value to clean

		Returns:
			any
		"""
		pass

	@classmethod
	def create(cls, details: dict):
		"""Create

		Figure out the child node type necessary and create an instance of it

		Arguments:
			details (dict): An object describing a data point

		Returns:
			any
		"""

		# If it's an array, create a list of options
		if isinstance(details, list):
			return cls.__classes.options(details)

		# Else if we got an object
		elif isinstance(details, dict):

			# If array is present
			if '__array__' in details:
				return cls.__classes.array(details, False)

			# Else if we have a hash
			elif '__hash__' in details:
				return cls.__classes.hash(details, False);

			# Else if we have a type
			elif '__type__' in details:

				# If the type is an object or an array, this is a complex type
				if isinstance(details['__type__'], dict) or isinstance(details['__type__'], list):
					return cls.create(details.__type__)

				# Else it's just a Node
				else:
					return cls.__classes.node(details, False);

			# Else it's most likely a parent
			else:
				return cls.__classes.parent(details, False)

		# Else if we got a string, use the value as the type
		elif isinstance(details, str):
			return cls.__classes.node(details, False)

		# Else, raise an error
		else:
			raise ValueError('details in %s.%s' % (
				cls.__name__,
				sys._getframe().f_code.co_name
			))

	@classmethod
	def from_file(cls, filename: str):
		"""From File

		Loads a JSON file and creates a Node instance from it

		Arguments:
			filename (str): The filename to load

		Returns:
			Base
		"""

		# Load the file
		oFile = open(filename)

		# Convert it to a dictionary
		dDetails = jsonb.decodef(oFile)

		# Create and return the new instance
		return cls(dDetails)

	def optional(self, value: bool | None = None):
		"""Optional

		Getter/Setter method for optional flag

		Arguments:
			value (bool): If set, the method is a setter

		Returns:
			bool | None
		"""

		# If there's no value, this is a getter
		if value is None:
			return self._optional

		# Else, set the flag
		else:
			self._optional = value and True or False

	@classmethod
	def register(cls, name: dict | str, constructor: any = None):
		"""Register

		Registers the classes that can be children because we can't require them
		in this file as webpack can't handle file A that requires file B that
		requires file A

		Arguments:
			name (dict | str): name/value object of all classes to register, or
								the name of the constructor that will be added
			constructor (callable) The class to associate with the given name

		Returns:
			None
		"""
		if isinstance(name, dict):
			cls.__classes = name
		else:
			cls.__classes[name] = constructor

	def special(self, name, value=None, default=None):
		"""Special

		Getter/Setter method for special values associated with nodes that are
		not fields

		To retrieve a value or values, pass only the name or names, to set a
		single special value, pass a name and value

		Args:
			name (str): The name of the value to either set or get
			value (mixed): The value to set
				Must be something that can be converted directly to JSON
			default (mixed): The default value
				Returned if the special field doesn't exist

		Returns:
			On getting, the value of the special field is returned. On setting,
			nothing is returned

		Raises:
			TypeError: If the name is not a valid string
			ValueError: If the name is invalid, or if setting and the value can
				not be converted to JSON
		"""

		# Check the name is a string
		if not isinstance(name, str):
			raise TypeError('name must be a string')

		# Check the name is valid
		if not constants.special.name.match(name):
			raise ValueError('special name must match "%s"' % constants.special.syntax)

		# If the value is not set, this is a getter
		if value is None:

			# Return the value or the default
			try:
				return copy.deepcopy(self._special[name])
			except KeyError:
				return default

		# Else, this is a setter
		else:

			# Can the value safely be turned into JSON
			try:
				jsonb.encode(value)
			except TypeError:
				raise ValueError('"%s" can not be encoded to JSON in %s.%s' % (
					self.__class__.__name__,
					sys._getframe().f_code.co_name
				))

			# Save it
			self.__special[name]	= value

	def to_dict(self):
		"""To Dict

		Returns the basic node as a dictionary in the same format as is used in
		constructing it

		Returns:
			dict
		"""

		# Create the dict we will return
		dRet = {}

		# If the optional flag is set
		if self._optional:
			dRet['__optional__'] = True

		# Add all the special fields found
		for k in self.__special.keys():
			dRet['__%s__' % k] = self.__special[k]

		# Return
		return dRet

	def to_json(self):
		"""To JSON

		Returns a JSON string representation of the instance

		Returns:
			str
		"""
		return jsonb.encode(self.to_dict())

	@abc.abstractmethod
	def valid(self, value, level=[]):
		"""Valid

		Checks if a value is valid based on the instance's values

		Args:
			value (mixed): The value to validate

		Returns:
			bool
		"""
		pass

	@property
	def validation_failures(self):
		"""Validation Failures

		Returns the last failures as a property so they can't be overwritten

		Returns:
			list
		"""
		return self._validation_failures