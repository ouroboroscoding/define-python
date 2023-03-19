# coding=utf8
"""Define

Define data structures
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Import local modules
from . import \
	array, \
	base, \
	constants as _constants, \
	hash

# Export the classes only
Array = array.Array
Base = base.Base
Hash = hash.Hash

# Re-export the constants
constants = _constants