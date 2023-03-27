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
	'constants',
	'Array', 'Base', 'Hash', 'Node', 'Options', 'Parent', 'Tree',
	'NOT_SET'
]

# Import local modules
from . import array, base, constants, hash, node, options, parent, tree

# Re-Export the classes
Array = array.Array
Base = base.Base
Hash = hash.Hash
Node = node.Node
Options = options.Options
Parent = parent.Parent
Tree = tree.Tree

# Re-Export not set variable
NOT_SET = base.NOT_SET