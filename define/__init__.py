# coding=utf8
"""Define

Define data structures
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Limit exports
__all__ = [
	'constants', 'NOT_SET',
	'Array', 'Base', 'Hash', 'Node', 'Options', 'Parent', 'Tree',
]

# Import jobject
import jobject

# Import local modules
from . import constants
from .array import Array
from .base import NOT_SET, Base
from .hash import Hash
from .node import Node
from .options import Options
from .parent import Parent
from .tree import Tree