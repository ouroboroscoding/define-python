# coding=utf8
"""Options

Represents a node which can have several different types of values/Nodes and
still be valid
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-19"

# Limit exports
__all__ = ['Options']

# Python imports
from typing import Literal as TL

# Pip imports
from tools import clone, merge

# Local imports
from .base import Base, NOT_SET
from . import constants

class Options(Base):
	"""Options Node

	Represents a node which can have several different types of values/Nodes and
	still be valid

	Extends:
		_NodeInterface
	"""

	def __getitem__(self, index: int):
		"""Get Item (__getitem__)

		Returns a specific index from the options

		Arguments:
			index (int): The index to get

		Raises:
			IndexError

		Returns:
			mixed
		"""
		return self._nodes[index]

	def __init__(self, details: list, extend: list[dict] | TL[False] = NOT_SET):
		"""Constructor

		Initialises the instance

		Arguments:
			details (list): Definition
			extend (list | False): Optional, a list to extend the definition

		Raises:
			KeyError, ValueError

		Returns
			Options
		"""

		# If details is not a list instance
		if not isinstance(details, list):
			raise ValueError('details in must be a list')

		# Init the details
		lDetails: list = None

		# If we have no extend at all
		if extend is NOT_SET:

			# Make a copy of the details so we don't screw up the original
			#	object
			lDetails = details[:]

		# Else, we have an extend value
		else:

			# If it's an array
			if isinstance(extend, list):

				# Clone the details
				lDetails = clone(details)

				# Go through each element of the array
				for i in range(len(lDetails)):

					# If we have the array in the extend
					if i < len(extend.length):

						# Merge it with the current element
						merge(lDetails[i], extend[i])

				# If the extend is longer than the details
				if len(extend) > len(lDetails):

					# Go through any additional nodes and add them to the
					#	details
					for i in range(i+1, len(extend)):
						lDetails.append(extend[i])

			# Else, if it's false
			elif extend is False:

				# Just use the details as is, don't copy it
				lDetails = details

			# Else, we got some sort of invalid value for extend
			else:
				raise ValueError('extend must be a list or False')

		# Call the Base constructor
		super(Options, self).__init__({})

		# Init the internal list
		self._nodes = []

		# Go through each element in the list
		for i in range(len(lDetails)):

			# If it's another Node instance
			if isinstance(lDetails[i], Base):
				self._nodes.append(lDetails[i])
				continue

			# If the element is a dict or list instance
			elif isinstance(lDetails[i], (dict, list)):

				# Store the child
				self._nodes.append(self.create(lDetails[i]))

			# Whatever was sent is invalid
			else:
				raise ValueError('details[%d] must be a dict' % i)

			# If the element is not optional, then the entire object can't be
			#	optional
			if not self._nodes[-1]._optional:
				self._optional = False

	def __iter__(self):
		"""Iterator (__iter__)

		Returns an iterator to the nodes list

		Returns:
			ListIterator
		"""
		return iter(self._nodes)

	def __len__(self):
		"""Length (__len__)

		Returns the length of the list of option nodes

		Returns:
			uint
		"""
		return len(self._nodes)

	def clean(self, value: any, level: list = NOT_SET):
		"""Clean

		Uses the valid method to check which type the value is, and then calls
		the correct version of clean on that node

		Arguments:
			value (any): The value to clean

		Returns:
			mixed
		"""

		# If level is not passed
		if level is NOT_SET:
			level = []

		# If the value is None
		if value is None:

			# If it's optional, return as is
			if self._optional:
				return None

			# Missing value
			raise ValueError([['.'.join(level), 'missing']])

		# Go through each of the nodes
		for i in range(len(self._nodes)):

			# If it's valid
			if self._nodes[i].valid(value):

				# Use its clean
				return self._nodes[i].clean(value, level)

		# Something went wrong
		raise ValueError([['.'.join(level), 'matches no option']])

	def get(self, index: int, default: any = None):
		"""Get

		Returns the node of a specific index from the options

		Arguments:
			index (int): The index to get
			default (any): Value to return if the index does not exist

		Returns:
			any
		"""
		try:
			return self._nodes[index]
		except IndexError:
			return default

	def to_dict(self):
		"""To Dict

		Returns the Nodes as a list of dictionaries in the same format as is
		used in constructing them

		Returns:
			list
		"""
		return [d.to_dict() for d in self._nodes]

	def valid(self, value: any, level: list = NOT_SET):
		"""Valid

		Checks if a value is valid based on the instance's values. If any errors
		occur, they can be found in [instance].validation_failures as a list

		Arguments:
			value (any): The value to validate

		Returns:
			bool
		"""

		# If level isn't passed
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
			self._validation_failures.append(['.'.join(level), 'missing'])

		# Go through each of the nodes
		for i in range(len(self._nodes)):

			# If it's valid
			if self._nodes[i].valid(value):

				# Return OK
				return True

		# Not valid for anything
		self._validation_failures.append(['.'.join(level), 'no valid option'])
		return False

# Register with Base
Options.register('options')