# coding=utf8
"""Define Tests

Used for testing the package"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Import python core modules
import datetime
from decimal import Decimal
import hashlib
import json

# Import define
import define

# Import unittest
import unittest

class define_Test(unittest.TestCase):

	def test_Array_Valid(self):

		# Create an array that only allows uniques
		a	= define.Array({
			'__array__':	'unique',
			'__type__':		'decimal'
		})

		# Check for true
		self.assertTrue(a.valid([Decimal('0.3'),Decimal('2.4'),Decimal('3.5'),Decimal('4.6')]), '[Decimal("0.3"),Decimal("2.4"),Decimal("3.5"),Decimal("4.6")] is not a valid unique decimal array')
		self.assertTrue(a.valid([Decimal('0.1'),Decimal('0.11'),Decimal('0.111'),Decimal('0.1111')]), '[Decimal("0.1"),Decimal("0.11"),Decimal("0.111"),Decimal("0.1111")] is not a valid unique decimal array')

		# Check for false
		self.assertFalse(a.valid([Decimal('2'),Decimal('2'),Decimal('3')]), '[Decimal("2"),Decimal("2"),Decimal("3")] is a valid unique decimal array')
		self.assertTrue(a.validation_failures[0][0] == '[1]', 'fail name is not correct: ' + str(a.validation_failures[0][0]))
		self.assertTrue(a.validation_failures[0][1] == 'duplicate of [0]', 'fail value is not correct: ' + str(a.validation_failures[0][1]))

		# Create an array that allows duplicates
		a	= define.Array({
			'__array__':	'duplicates',
			'__type__':		'decimal'
		})

		# Check for true
		self.assertTrue(a.valid([Decimal('0.3'),Decimal('2.4'),Decimal('0.3'),Decimal('4.6')]), '[Decimal("0.3"),Decimal("2.4"),Decimal("0.3"),Decimal("4.6")] is not a valid decimal array')
		self.assertTrue(a.valid([Decimal('0.1'),Decimal('0.11'),Decimal('0.1'),Decimal('0.1111')]), '[Decimal("0.1"),Decimal("0.11"),Decimal("0.1"),Decimal("0.1111")] is not a valid decimal array')

		# Check for false
		self.assertFalse(a.valid(['Hello',2,3]), '["Hello",2,3] is a valid unique decimal array')
		self.assertTrue(a.validation_failures[0][0] == '[0]', 'fail name is not correct: ' + str(a.validation_failures[0][0]))
		self.assertTrue(a.validation_failures[0][1] == 'can not be converted to decimal', 'fail value is not correct: ' + str(a.validation_failures[0][1]))

	def test_Complex(self):

		# Create a complex structure with all types of data just to make sure
		#	everything runs as expected. We don't need to test/verify the data,
		#	as the other methods will do that. This is more to make sure multi-
		#	level structures work as expected by calling each other
		oComplex = define.Tree({
			"__name__": "Complex",
			"array": {
				"__array__": "unique",
				"__type__": {
					"string": {"__type__": "string"},
					"unsigned": {"__type__": "uint"},
					"date": {"__type__": "date"}
				}
			},
			"hash": {
				"__hash__": "uuid",
				"__type__": {
					"boolean": {"__type__": "bool"},
					"price": {"__type__": "price"},
					"float": {"__type__": "float"}
				}
			},
			"options": [
				{"__type__": "date"},
				{"__type__": "datetime"}
			],
			"parent": {
				"any": {"__type__": "any"},
				"base64": {"__type__": "base64"},
				"parent_again": {
					"integer": {"__type__": "int"},
					"md5": {"__type__": "md5"}
				}
			}
		})

		# Create an instance
		dComplex = {
			"array": [
				{"string": "Hello", "unsigned": 100, "date": "2022-01-01"},
				{"string": "There", "unsigned": 0, "date": "1981-05-02"},
				{"string": "Friend", "unsigned": 13, "date": "1950-04-23"}
			],
			"hash": {
				"52cd4b20-ca32-4433-9516-0c8684ec57c2": {
					"boolean": True, "price": "9.99", "float": 9.9
				},
				"3b44c5ed-0fea-4478-9f1b-939ae6ec0721": {
					"boolean": False, "price": "0.99", "float": 0.999
				},
				"6432b16a-7e27-47cd-8360-82d82ac70078": {
					"boolean": True, "price": "10.00", "float": 10.01
				}
			},
			"options": "2000-12-23",
			"parent": {
				"any": None,
				"base64": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==",
				"parent_again": {
					"integer": -10,
					"md5": "7b967af699a0a18b1f2bdc9704537a3e"
				}
			}
		}

		# Clean
		oComplex.clean(dComplex)

		# Validate
		oComplex.valid(dComplex)

		# Create another instance
		dComplex = {
			"array": [
				{"string": "Stuff", "unsigned": 7676, "date": "3000-06-01"}
			],
			"hash": {
				"6432b16a-7e27-47cd-8360-82d82ac70078": {
					"boolean": False, "price": "0.01", "float": .000001
				}
			},
			"options": "2000-12-23 12:23:05",
			"parent": {
				"any": None,
				"base64": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==",
				"parent_again": {
					"integer": 0,
					"md5": "7b967af699a0a18b1f2bdc9704537a3e"
				}
			}
		}

		# Clean
		oComplex.clean(dComplex)

		# Validate
		oComplex.valid(dComplex)

	def test_Hash_Hash_Valid(self):

		# Create a hash of hashes
		oHash = define.Hash({
			"__hash__":"string",
			"__type__":{
				"__hash__":"string",
				"__type__":"uint"
			}
		})

		# Check for true
		self.assertTrue(oHash.valid({
			"test":{
				"un":1,
				"deux":2,
				"trois":3
			},
			"this":{
				"one":1,
				"two":2,
				"three":3
			}
		}), "hash of hashes failed validation")

		# Check for false
		self.assertFalse(oHash.valid({
			"test":{
				"un":1,
				"deux":2,
				"trois":3
			},
			"me":1
		}), "Invalid hash of hashes deemed valid")

	def test_Node_Clean(self):

		# Create a basic any Node
		oNode	= define.Node({
			"__type__":	"any"
		})

		# Check for True
		self.assertTrue(oNode.clean(0) == 0, '0 does not equal 0')
		self.assertTrue(oNode.clean(0.1) == 0.1, '0.1 does not equal 0.1')
		self.assertTrue(oNode.clean('0') == '0', '"0" does not equal "0"')
		self.assertTrue(oNode.clean(True) == True, 'True does not equal True')
		self.assertTrue(oNode.clean([]) == [], '[] does not equal []')
		self.assertTrue(oNode.clean({}) == {}, '{} does not equal {}')

		# Create a basic bool Node
		oNode	= define.Node({
			"__type__":	"bool"
		})

		# Check for True
		self.assertTrue(oNode.clean(True) == True, 'True does not equal True')
		self.assertTrue(oNode.clean(False) == False, 'False does not equal False')
		self.assertTrue(oNode.clean('1') == True, '"1" does not equal True')
		self.assertTrue(oNode.clean('0') == False, '"0" does not equal False')
		self.assertTrue(oNode.clean('Y') == True, '"Y" does not equal True')
		self.assertTrue(oNode.clean('') == False, '"" does not equal False')
		self.assertTrue(oNode.clean(1) == True, '1 does not equal True')
		self.assertTrue(oNode.clean(0) == False, '0 does not equal False')
		self.assertTrue(oNode.clean(0.1) == True, '0.1 does not equal True')
		self.assertTrue(oNode.clean(0.0) == False, '0.0 does not equal False')

		# Create a basic date Node
		oNode	= define.Node({
			"__type__":	"date"
		})

		# Check for True
		self.assertTrue(oNode.clean('0000-00-00') == '0000-00-00', '"0000-00-00" does not equal "0000-00-00"')
		self.assertTrue(oNode.clean('1981-05-02') == '1981-05-02', '"1981-05-02" does not equal "1981-05-02"')
		self.assertTrue(oNode.clean(datetime.date(1981,5,2)) == '1981-05-02', 'datetime.date(1981,5,2) does not equal "1981-05-02"')
		self.assertTrue(oNode.clean(datetime.datetime(1981,5,2,12,23,0)) == '1981-05-02', 'datetime.date(1981,5,2,12,23,0) does not equal "1981-05-02"')

		# Create a basic datetime Node
		oNode	= define.Node({
			"__type__":	"datetime"
		})

		# Check for True
		self.assertTrue(oNode.clean('0000-00-00 00:00:00') == '0000-00-00 00:00:00', '"0000-00-00 00:00:00" does not equal "0000-00-00 00:00:00"')
		self.assertTrue(oNode.clean('1981-05-02 12:23:00') == '1981-05-02 12:23:00', '"1981-05-02 12:23:00" does not equal "1981-05-02 12:23:00"')
		self.assertTrue(oNode.clean(datetime.date(1981,5,2)) == '1981-05-02 00:00:00', 'datetime.date(1981,5,2) does not equal "1981-05-02 00:00:00"')
		self.assertTrue(oNode.clean(datetime.datetime(1981,5,2,12,23,0)) == '1981-05-02 12:23:00', 'datetime.date(1981,5,2,12,23,0) does not equal "1981-05-02 12:23:00"')

		# Create a basic decimal Node
		oNode	= define.Node({
			"__type__":	"decimal"
		})

		self.assertTrue(oNode.clean('0.0') == '0.0', '"0.0" does not equal "0.0"')
		self.assertTrue(oNode.clean('3.14') == '3.14', '"3.14" does not equal "3.14"')
		self.assertTrue(oNode.clean('-3.14') == '-3.14', '"-3.14" does not equal "-3.14"')
		self.assertTrue(oNode.clean(3) == '3', '3 does not equal "3.0"')
		self.assertTrue(oNode.clean('3') == '3', '"3" does not equal "3.0"')

		# Create a basic float Node
		oNode	= define.Node({
			"__type__":	"float"
		})

		self.assertTrue(oNode.clean(0.0) == 0.0, '0.0 does not equal 0.0')
		self.assertTrue(oNode.clean(3.14) == 3.14, '3.14 does not equal 3.14')
		self.assertTrue(oNode.clean(-3.14) == -3.14, '-3.14 does not equal -3.14')
		self.assertTrue(oNode.clean('0.0') == 0.0, '"0.0" does not equal 0.0')
		self.assertTrue(oNode.clean('3.14') == 3.14, '"3.14" does not equal 3.14')
		self.assertTrue(oNode.clean('-3.14') == -3.14, '"-3.14" does not equal -3.14')
		self.assertTrue(oNode.clean(3) == 3.0, '3 does not equal 3.0')
		self.assertTrue(oNode.clean('3') == 3.0, '"3" does not equal 3.0')

		# Create a basic int Node
		oNode	= define.Node({
			"__type__":	"int"
		})

		# Check for True
		self.assertTrue(oNode.clean(0) == 0, '0 does not equal 0')
		self.assertTrue(oNode.clean(1) == 1, '1 does not equal 1')
		self.assertTrue(oNode.clean(-1) == -1, '-1 does not equal -1')
		self.assertTrue(oNode.clean(3.14) == 3, '3.14 does not equal 3')
		self.assertTrue(oNode.clean(3) == 3, '3 does not equal 3')
		self.assertTrue(oNode.clean('3') == 3, '"3" does not equal 3')
		self.assertTrue(oNode.clean('-3') == -3, '"-3" does not equal -3')
		self.assertTrue(oNode.clean('0o76') == 62, "076 does not equal 62")
		self.assertTrue(oNode.clean('0x3E') == 62, "0x3E does not equal 62")

		# Create a basic ip Node
		oNode	= define.Node({
			"__type__":	"ip"
		})

		# Check for True
		self.assertTrue(oNode.clean('127.0.0.1') == '127.0.0.1', '"127.0.0.1" does not equal "127.0.0.1"')
		self.assertTrue(oNode.clean('10.0.0.1') == '10.0.0.1', '"10.0.0.1" does not equal "10.0.0.1"')
		self.assertTrue(oNode.clean('255.255.255.255') == '255.255.255.255', '"255.255.255.255" does not equal "255.255.255.255"')

		# Create a basic json Node
		oNode	= define.Node({
			"__type__":	"json"
		})

		# Check for True
		self.assertTrue(oNode.clean('{"hello":"there"}') == '{"hello":"there"}', '"{"hello":"there"}" does not equal "{"hello":"there"}"')
		self.assertTrue(oNode.clean('"hello"') == '"hello"', '"hello" does not equal "hello"')
		self.assertTrue(oNode.clean({"Hello":"there"}) == '{"Hello": "there"}', '{"Hello":"there"} does not equal "{"Hello": "there"}"')
		self.assertTrue(oNode.clean([1,2,34]) == '[1, 2, 34]', '[1,2,34] does not equal "[1,2,34]"')

		# Create a basic md5 Node
		oNode	= define.Node({
			"__type__":	"md5"
		})

		# Check for True
		self.assertTrue(oNode.clean('65a8e27d8879283831b664bd8b7f0ad4') == '65a8e27d8879283831b664bd8b7f0ad4', '"65a8e27d8879283831b664bd8b7f0ad4" does not equal "65a8e27d8879283831b664bd8b7f0ad4"')
		self.assertTrue(oNode.clean(hashlib.md5(b'Hello, World!')) == '65a8e27d8879283831b664bd8b7f0ad4', '"hello" does not equal "hello"')

		# Create a basic price Node
		oNode	= define.Node({
			"__type__":	"price"
		})

		self.assertTrue(oNode.clean(0.0) == '0.00', '0.0 does not equal "0.00"')
		self.assertTrue(oNode.clean('0.0') == '0.00', '"0.0" does not equal "0.00"')
		self.assertTrue(oNode.clean('3.1') == '3.10', '"3.1" does not equal "3.10"')
		self.assertTrue(oNode.clean('-3.1') == '-3.10', '"-3.1" does not equal "-3.10"')
		self.assertTrue(oNode.clean('3.14') == '3.14', '"3.14" does not equal "3.14"')
		self.assertTrue(oNode.clean('-3.14') == '-3.14', '"-3.14" does not equal "-3.14"')
		self.assertTrue(oNode.clean(3) == '3.00', '3 does not equal "3.00"')
		self.assertTrue(oNode.clean('3') == '3.00', '"3" does not equal "3.00"')

		# Create a basic string Node
		oNode	= define.Node({
			"__type__":	"string"
		})

		# Check for True
		self.assertTrue(oNode.clean('127.0.0.1') == '127.0.0.1', '"127.0.0.1" does not equal "127.0.0.1"')
		self.assertTrue(oNode.clean('10.0.0.1') == '10.0.0.1', '"10.0.0.1" does not equal "10.0.0.1"')
		self.assertTrue(oNode.clean('255.255.255.255') == '255.255.255.255', '"255.255.255.255" does not equal "255.255.255.255"')
		self.assertTrue(oNode.clean(0) == '0', '0 does not equal "0"')
		self.assertTrue(oNode.clean(0.0) == '0.0', '0.0 does not equal "0.0"')
		self.assertTrue(oNode.clean(3.14) == '3.14', '3.14 does not equal "3.14"')
		self.assertTrue(oNode.clean(datetime.date(1981,5,2)) == '1981-05-02', 'datetime.date(1981,5,2) does not equal "1981-05-02"')

		# Create a basic time Node
		oNode	= define.Node({
			"__type__":	"time"
		})

		# Check for True
		self.assertTrue(oNode.clean('00:00:00') == '00:00:00', '"0000-00-00 00:00:00" does not equal "00:00:00"')
		self.assertTrue(oNode.clean('12:23:00') == '12:23:00', '"1981-05-02 12:23:00" does not equal "12:23:00"')
		self.assertTrue(oNode.clean(datetime.time(12,23,0)) == '12:23:00', 'datetime.time(12,23,0) does not equal "12:23:00"')
		self.assertTrue(oNode.clean(datetime.datetime(1981,5,2,12,23,0)) == '12:23:00', 'datetime.date(1981,5,2,12,23,0) does not equal "12:23:00"')

		# Create a basic timestamp Node
		oNode	= define.Node({
			"__type__":	"timestamp"
		})

		# Check for True
		self.assertTrue(oNode.clean(0) == 0, '0 does not equal 0')
		self.assertTrue(oNode.clean(1) == 1, '1 does not equal 1')
		self.assertTrue(oNode.clean(3.14) == 3, '3.14 does not equal 3')
		self.assertTrue(oNode.clean(3) == 3, '3 does not equal 3')
		self.assertTrue(oNode.clean('3') == 3, '"3" does not equal 3')

		# Create a basic uint Node
		oNode	= define.Node({
			"__type__":	"uint"
		})

		# Check for True
		self.assertTrue(oNode.clean(0) == 0, '0 does not equal 0')
		self.assertTrue(oNode.clean(1) == 1, '1 does not equal 1')
		self.assertTrue(oNode.clean(3.14) == 3, '3.14 does not equal 3')
		self.assertTrue(oNode.clean(3) == 3, '3 does not equal 3')
		self.assertTrue(oNode.clean('3') == 3, '"3" does not equal 3')

		# Create a basic uuid Node
		oNode	= define.Node({
			"__type__":	"uuid"
		})

		self.assertTrue(oNode.clean('52cd4b20-ca32-4433-9516-0c8684ec57c2') == '52cd4b20-ca32-4433-9516-0c8684ec57c2', '"52cd4b20-ca32-4433-9516-0c8684ec57c2" does not equal "52cd4b20-ca32-4433-9516-0c8684ec57c2"')
		self.assertTrue(oNode.clean('3b44c5ed-0fea-4478-9f1b-939ae6ec0721') == '3b44c5ed-0fea-4478-9f1b-939ae6ec0721', '"3b44c5ed-0fea-4478-9f1b-939ae6ec0721" does not equal "3b44c5ed-0fea-4478-9f1b-939ae6ec0721"')
		self.assertTrue(oNode.clean('6432b16a-7e27-47cd-8360-82d82ac70078') == '6432b16a-7e27-47cd-8360-82d82ac70078', '"6432b16a-7e27-47cd-8360-82d82ac70078" does not equal "6432b16a-7e27-47cd-8360-82d82ac70078"')


	def test_Node_Valid_Basic(self):

		# Create a new basic any Node module
		oNode	 = define.Node({
			'__type__':	'any'
		})

		# Check for True
		self.assertTrue(oNode.valid(1), '1 is not a valid any')
		self.assertTrue(oNode.valid(0), '0 is not a valid any')
		self.assertTrue(oNode.valid(-1), '-1 is not a valid any')
		self.assertTrue(oNode.valid('0'), '"0" is not a valid any')
		self.assertTrue(oNode.valid('1'), '"1" is not a valid any')
		self.assertTrue(oNode.valid('-1'), '"-1" is not a valid any')
		self.assertTrue(oNode.valid('0xff'), '"0xff" is not a valid any')
		self.assertTrue(oNode.valid('0o7'), '"0o7" is not a valid any')
		self.assertTrue(oNode.valid('Hello'), '"Hello" is not a valid any')
		self.assertTrue(oNode.valid(True), 'True is not a valid any')
		self.assertTrue(oNode.valid(0.1), '0.1 is not a valid any')
		self.assertTrue(oNode.valid(Decimal('0.1')), 'Decimal("0.1") is not a valid any')
		self.assertTrue(oNode.valid('192.168.0.1'), '"192.168.0.1" is not a valid any')
		self.assertTrue(oNode.valid('2016-03-05'), '"2016-03-05" is not a valid any')
		self.assertTrue(oNode.valid('13:50:00'), '"13:50:00" is not a valid any')
		self.assertTrue(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is not a valid any')
		self.assertTrue(oNode.valid([]), '[] is not a valid any')
		self.assertTrue(oNode.valid({}), '{} is not a valid any')

		# Create a new basic base64 Node module
		oNode	 = define.Node({
			'__type__':	'base64'
		})

		# Check for True
		self.assertTrue(oNode.valid('SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ=='), '"SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==" is not a valid base64')
		self.assertTrue(oNode.valid('WW8gWW8gWW8='), '"WW8gWW8gWW8=" is not a valid base64')
		self.assertTrue(oNode.valid('RG92ZXRhaWwgaXMgdGhlIHNoaXQu'), '"RG92ZXRhaWwgaXMgdGhlIHNoaXQu" is not a valid base64')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid base64')
		self.assertFalse(oNode.valid('WW8gWW8gWW8==='), '"WW8gWW8gWW8===" is a valid base64')
		self.assertFalse(oNode.valid(''), '"" is a valid base64')

		# Create a new basic bool Node module
		oNode	 = define.Node({
			'__type__':	'bool'
		})

		# Check for True
		self.assertTrue(oNode.valid(True), 'True is not a valid bool')
		self.assertTrue(oNode.valid(False), 'False is not a valid bool')
		self.assertTrue(oNode.valid(1), '1 is not a valid bool')
		self.assertTrue(oNode.valid(0), '0 is not a valid bool')
		for s in ['true', 'True', 'TRUE', 't', 'T', '1', 'false', 'False', 'FALSE', 'f', 'F', '0']:
			self.assertTrue(oNode.valid(s), '"' + s + '" is not a valid bool')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid bool')
		self.assertFalse(oNode.valid(2), '2 is a valid bool')
		self.assertFalse(oNode.valid(1.2), '1.2 is a valid bool')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid bool')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid bool')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid bool')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid bool')
		self.assertFalse(oNode.valid([]), '[] is a valid bool')
		self.assertFalse(oNode.valid({}), '{} is a valid bool')

		# Create a new basic date Node module
		oNode	 = define.Node({
			'__type__':	'date'
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-03-05'), '"2016-03-05" is not a valid date')
		self.assertTrue(oNode.valid('2020-12-25'), '"2020-12-25" is not a valid date')
		self.assertTrue(oNode.valid('1970-01-01'), '"1970-01-01" is not a valid date')
		self.assertTrue(oNode.valid(datetime.date(1981,5,2)), 'datetime.date(1981,5,2) is not a valid date')
		self.assertTrue(oNode.valid(datetime.datetime(1981,5,2,12,23,0)), 'datetime.datetime(1981,5,2,12,23,0) is not a valid date')

		# Check for False
		self.assertFalse(oNode.valid('70-01-01'), '"70-01-01" is a valid date')
		self.assertFalse(oNode.valid('10000-01-01'), '"10000-01-01" is a valid date')
		self.assertFalse(oNode.valid('1970-00-01'), '"1970-00-01" is a valid date')
		self.assertFalse(oNode.valid('2000-12-00'), '"2000-12-00" is a valid date')
		self.assertFalse(oNode.valid('2000-12-32'), '"2000-12-32" is a valid date')
		self.assertFalse(oNode.valid('2000-13-10'), '"2000-13-10" is a valid date')
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid date')
		self.assertFalse(oNode.valid(True), 'True is a valid date')
		self.assertFalse(oNode.valid(2), '2 is a valid date')
		self.assertFalse(oNode.valid(1.2), '1.2 is a valid date')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid date')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid date')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid date')
		self.assertFalse(oNode.valid([]), '[] is a valid date')
		self.assertFalse(oNode.valid({}), '{} is a valid date')

		# Create a new basic datetime Node module
		oNode	 = define.Node({
			'__type__':	'datetime'
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-03-05 10:04:00'), '"10:04:00" is not a valid datetime')
		self.assertTrue(oNode.valid('2020-12-25 00:00:00'), '"00:00:00" is not a valid datetime')
		self.assertTrue(oNode.valid('2020-12-25 12:23:34'), '"12:23:34" is not a valid datetime')
		self.assertTrue(oNode.valid('1970-01-01 02:56:12'), '"02:56:12" is not a valid datetime')
		self.assertTrue(oNode.valid(datetime.date(1981,5,2)), 'datetime.date(1981,5,2) is not a valid datetime')
		self.assertTrue(oNode.valid(datetime.datetime(1981,5,2,12,23,0)), 'datetime.datetime(1981,5,2,12,23,0) is not a valid datetime')

		# Check for False
		self.assertFalse(oNode.valid('2016-03-05 1:00:00'), '"2016-03-05 1:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05 100:01:00'), '"2016-03-05 100:01:00" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05 24:00:00'), '"2016-03-05 24:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05 00:0:00'), '"2016-03-05 00:0:00" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05 00:00:0'), '"2016-03-05 00:00:0" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05 23:60:00'), '"2016-03-05 23:60:00" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05 23:00:60'), '"2016-03-05 23:00:60" is a valid datetime')
		self.assertFalse(oNode.valid('70-01-01 00:00:00'), '"70-01-01 00:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('10000-01-01 00:00:00'), '"10000-01-01 00:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('1970-00-01 00:00:00'), '"1970-00-01 00:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('2000-12-00 00:00:00'), '"2000-12-00 00:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('2000-12-32 00:00:00'), '"2000-12-00 00:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('2000-13-10 00:00:00'), '"2000-12-00 00:00:00" is a valid datetime')
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid datetime')
		self.assertFalse(oNode.valid(True), 'True is a valid datetime')
		self.assertFalse(oNode.valid(2), '2 is a valid datetime')
		self.assertFalse(oNode.valid(1.2), '1.2 is a valid datetime')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid datetime')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid datetime')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid decimal')
		self.assertFalse(oNode.valid([]), '[] is a valid datetime')
		self.assertFalse(oNode.valid({}), '{} is a valid datetime')

		# Create a new basic decimal Node module
		oNode	 = define.Node({
			'__type__':	'decimal'
		})

		# Check for True
		self.assertTrue(oNode.valid(Decimal('1.0')), 'Decimal("1.0") is not a valid decimal')
		self.assertTrue(oNode.valid(Decimal('1.1')), 'Decimal("1.1") is not a valid decimal')
		self.assertTrue(oNode.valid(-0.1), '-0.1 is not a valid decimal')
		self.assertTrue(oNode.valid(1), '1 is not a valid decimal')
		self.assertTrue(oNode.valid(0), '0 is not a valid decimal')
		self.assertTrue(oNode.valid(-1), '-1 is not a valid decimal')
		self.assertTrue(oNode.valid('1.0'), '"0" is not a valid decimal')
		self.assertTrue(oNode.valid('1.1'), '"0" is not a valid decimal')
		self.assertTrue(oNode.valid('-0.1'), '"0" is not a valid decimal')
		self.assertTrue(oNode.valid('0'), '"0" is not a valid decimal')
		self.assertTrue(oNode.valid('1'), '"1" is not a valid decimal')
		self.assertTrue(oNode.valid('-1'), '"-1" is not a valid decimal')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid decimal')
		self.assertFalse(oNode.valid(True), 'True is a valid decimal')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid decimal')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid decimal')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid decimal')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid decimal')
		self.assertFalse(oNode.valid([]), '[] is a valid decimal')
		self.assertFalse(oNode.valid({}), '{} is a valid decimal')

		# Create a new basic float Node module
		oNode	 = define.Node({
			'__type__':	'float'
		})

		# Check for True
		self.assertTrue(oNode.valid(1.0), '1.0 is not a valid float')
		self.assertTrue(oNode.valid(0.0), '0.0 is not a valid float')
		self.assertTrue(oNode.valid(-1.0), '-1.0 is not a valid float')
		self.assertTrue(oNode.valid('1.0'), '"1.0" is not a valid float')
		self.assertTrue(oNode.valid('0.0'), '"0.0" is not a valid float')
		self.assertTrue(oNode.valid('-1.0'), '"-1.0" is not a valid float')
		self.assertTrue(oNode.valid(1), '1 is not a valid float')
		self.assertTrue(oNode.valid(0), '0 is not a valid float')
		self.assertTrue(oNode.valid(-1), '-1 is not a valid float')
		self.assertTrue(oNode.valid('0'), '"0" is not a valid float')
		self.assertTrue(oNode.valid('1'), '"1" is not a valid float')
		self.assertTrue(oNode.valid('-1'), '"-1" is not a valid float')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid float')
		self.assertFalse(oNode.valid(True), 'True is a valid float')
		self.assertFalse(oNode.valid('0xff'), '"0xff" is a valid float')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid float')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid float')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid float')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid float')
		self.assertFalse(oNode.valid([]), '[] is a valid float')
		self.assertFalse(oNode.valid({}), '{} is a valid float')

		# Create a new basic int Node module
		oNode	 = define.Node({
			'__type__':	'int'
		})

		# Check for True
		self.assertTrue(oNode.valid(1), '1 is not a valid int')
		self.assertTrue(oNode.valid(0), '0 is not a valid int')
		self.assertTrue(oNode.valid(-1), '-1 is not a valid int')
		self.assertTrue(oNode.valid('0'), '"0" is not a valid int')
		self.assertTrue(oNode.valid('1'), '"1" is not a valid int')
		self.assertTrue(oNode.valid('-1'), '"-1" is not a valid int')
		self.assertTrue(oNode.valid('0xff'), '"0xff" is not a valid int')
		self.assertTrue(oNode.valid('0o7'), '"0o7" is not a valid int')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid int')
		self.assertFalse(oNode.valid(True), 'True is a valid int')
		self.assertFalse(oNode.valid(0.1), '0.1 is a valid int')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid int')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid int')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid int')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid int')
		self.assertFalse(oNode.valid([]), '[] is a valid int')
		self.assertFalse(oNode.valid({}), '{} is a valid int')

		# Create a new basic IP Node module
		oNode	 = define.Node({
			'__type__':	'ip'
		})

		# Check for True
		self.assertTrue(oNode.valid('192.168.0.1'), '"192.168.0.1" is not a valid ip')
		self.assertTrue(oNode.valid('10.13.13.1'), '"10.13.13.1" is not a valid ip')
		self.assertTrue(oNode.valid('255.255.255.255'), '"255.255.255.255" is not a valid ip')
		self.assertTrue(oNode.valid('8.8.8.8'), '"8.8.8.8" is not a valid ip')
		self.assertTrue(oNode.valid('66.36.159.171'), '"66.36.159.171" is not a valid ip')
		self.assertTrue(oNode.valid('255.255.255.0'), '"255.255.255.0" is not a valid ip')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid ip')
		self.assertFalse(oNode.valid(True), 'True is a valid ip')
		self.assertFalse(oNode.valid(0), '0 is a valid ip')
		self.assertFalse(oNode.valid(0.1), '0.1 is a valid ip')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid ip')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid ip')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid ip')
		self.assertFalse(oNode.valid([]), '[] is a valid ip')
		self.assertFalse(oNode.valid({}), '{} is a valid ip')

		# Create a new basic JSON Node module
		oNode	 = define.Node({
			'__type__':	'json'
		})

		# Check for True
		self.assertTrue(oNode.valid('{"hello":"there","my":1,"true":3.14}'), '{"hello":"there","my":1,"true":3.14} is not valid json')
		self.assertTrue(oNode.valid('{"hello":[1,2,34],"my":1,"true":true}'), '{"hello":[1,2,34],"my":1,"true":true} is not valid json')
		self.assertTrue(oNode.valid('["a","b","c","d"]'), '["a","b","c","d"] is not valid json')
		self.assertTrue(oNode.valid('"Hello"'), '"Hello" is not valid json')
		self.assertTrue(oNode.valid('true'), 'true is not valid json')
		self.assertTrue(oNode.valid(1), '1 is not valid json')
		self.assertTrue(oNode.valid(0), '0 is not valid json')
		self.assertTrue(oNode.valid(-1), '-1 is not valid json')
		self.assertTrue(oNode.valid('0'), '"0" is not valid json')
		self.assertTrue(oNode.valid('1'), '"1" is not valid json')
		self.assertTrue(oNode.valid('-1'), '"-1" is not valid json')
		self.assertTrue(oNode.valid(True), 'True is not valid json')
		self.assertTrue(oNode.valid(0.1), '0.1 is not valid json')
		self.assertTrue(oNode.valid([]), '[] is not valid json')
		self.assertTrue(oNode.valid({}), '{} is not valid json')

		# Check for False
		self.assertFalse(oNode.valid('{\'hello\':\'there\'}'), '{\'hello\':\'there\'} is valid json')
		self.assertFalse(oNode.valid('{hello:[1,2,34]}'), '{hello:[1,2,34]} is valid json')
		self.assertFalse(oNode.valid('"a","b","c","d"'), '"a","b","c","d" is valid json')
		self.assertFalse(oNode.valid('Hello'), '"Hello" is valid json')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is valid json')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is valid json')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is valid json')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is valid json')

		# Create a new basic md5 Node module
		oNode	 = define.Node({
			'__type__':	'md5'
		})

		# Check for True
		self.assertTrue(oNode.valid('7b967af699a0a18b1f2bdc9704537a3e'), '"7b967af699a0a18b1f2bdc9704537a3e" is not a valid md5')
		self.assertTrue(oNode.valid('889ffd8cc409445187c4258d138192b6'), '"889ffd8cc409445187c4258d138192b6" is not a valid md5')
		self.assertTrue(oNode.valid('49c0d2aef0ab2634b0051544cdbf2415'), '"49c0d2aef0ab2634b0051544cdbf2415" is not a valid md5')
		self.assertTrue(oNode.valid('65a8e27d8879283831b664bd8b7f0ad4'), '"65a8e27d8879283831b664bd8b7f0ad4" is not a valid md5')
		self.assertTrue(oNode.valid('746b975324b133ceb2e211af41c049e8'), '"746b975324b133ceb2e211af41c049e8" is not a valid md5')
		self.assertTrue(oNode.valid(hashlib.md5(b'Hello, World!')), 'hashlib.md5("Hello, World!") is not a valid md5')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid md5')
		self.assertFalse(oNode.valid(True), '"Hello" is a valid md5')
		self.assertFalse(oNode.valid(0), '0 is a valid md5')
		self.assertFalse(oNode.valid(0.1), '0.1 is a valid md5')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid md5')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid md5')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid md5')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid md5')
		self.assertFalse(oNode.valid([]), '[] is a valid md5')
		self.assertFalse(oNode.valid({}), '{} is a valid md5')

		# Create a new basic price Node module
		oNode	 = define.Node({
			'__type__':	'price'
		})

		# Check for True
		self.assertTrue(oNode.valid(Decimal('1.0')), 'Decimal("1.0") is not a valid price')
		self.assertTrue(oNode.valid(Decimal('1.1')), 'Decimal("1.1") is not a valid price')
		self.assertTrue(oNode.valid(Decimal('-0.1')), 'Decimal("0.1") is not a valid price')
		self.assertTrue(oNode.valid(1), '1 is not a valid price')
		self.assertTrue(oNode.valid(0), '0 is not a valid price')
		self.assertTrue(oNode.valid(-1), '-1 is not a valid price')
		self.assertTrue(oNode.valid('1.0'), '"1.0" is not a valid price')
		self.assertTrue(oNode.valid('1.1'), '"1.1" is not a valid price')
		self.assertTrue(oNode.valid('-0.1'), '"-0.1" is not a valid price')
		self.assertTrue(oNode.valid('0'), '"0" is not a valid price')
		self.assertTrue(oNode.valid('1'), '"1" is not a valid price')
		self.assertTrue(oNode.valid('-1'), '"-1" is not a valid price')

		# Check for False
		self.assertFalse(oNode.valid(1.234), '1.234 is a valid price')
		self.assertFalse(oNode.valid('0.234'), '"0.234" is a valid price')
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid price')
		self.assertFalse(oNode.valid(True), 'True is a valid price')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid price')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid price')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid price')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid price')
		self.assertFalse(oNode.valid([]), '[] is a valid price')
		self.assertFalse(oNode.valid({}), '{} is a valid price')

		# Create a new basic string Node module
		oNode	 = define.Node({
			'__type__':	'string'
		})

		# Check for True
		self.assertTrue(oNode.valid('Hello, World!'), '"Hello, World!" is not a valid string')
		self.assertTrue(oNode.valid('0000000'), '"0000000" is not a valid string')
		self.assertTrue(oNode.valid('       '), '"	   " is not a valid string')
		self.assertTrue(oNode.valid('Why\nShould\nThis\nWork\n?'), '"Why\nShould\nThis\nWork\n?" is not a valid string')
		self.assertTrue(oNode.valid(u'unicode bitches'), 'u"unicode bitches" is not a valid string')
		self.assertTrue(oNode.valid('192.168.0.1'), '"192.168.0.1" is not a valid string')
		self.assertTrue(oNode.valid('2016-03-05'), '"2016-03-05" is not a valid string')
		self.assertTrue(oNode.valid('13:50:00'), '"13:50:00" is not a valid string')
		self.assertTrue(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is not a valid string')

		# Check for False
		self.assertFalse(oNode.valid(True), '"Hello" is a valid md5')
		self.assertFalse(oNode.valid(0), '"Hello" is a valid md5')
		self.assertFalse(oNode.valid(0.1), '0.1 is a valid md5')
		self.assertFalse(oNode.valid([]), '[] is a valid md5')
		self.assertFalse(oNode.valid({}), '{} is a valid md5')

		# Create a new basic time Node module
		oNode	 = define.Node({
			'__type__':	'time'
		})

		# Check for True
		self.assertTrue(oNode.valid('10:04:00'), '"10:04:00" is not a valid time')
		self.assertTrue(oNode.valid('00:00:00'), '"00:00:00" is not a valid time')
		self.assertTrue(oNode.valid('12:23:34'), '"12:23:34" is not a valid time')
		self.assertTrue(oNode.valid('02:56:12'), '"02:56:12" is not a valid time')
		self.assertTrue(oNode.valid(datetime.time(12,23,0)), 'datetime.time(12,23,0) is not a valid time')
		self.assertTrue(oNode.valid(datetime.datetime(1981,5,2,12,23,0)), 'datetime.datetime(1981,5,2,12,23,0) is not a valid time')

		# Check for False
		self.assertFalse(oNode.valid('1:00:00'), '"1:00:00" is a valid time')
		self.assertFalse(oNode.valid('100:01:00'), '"100:01:00" is a valid time')
		self.assertFalse(oNode.valid('24:00:00'), '"24:00:00" is a valid time')
		self.assertFalse(oNode.valid('00:0:00'), '"00:0:00" is a valid time')
		self.assertFalse(oNode.valid('00:00:0'), '"00:00:0" is a valid time')
		self.assertFalse(oNode.valid('23:60:00'), '"23:60:00" is a valid time')
		self.assertFalse(oNode.valid('23:00:60'), '"23:00:60" is a valid time')
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid time')
		self.assertFalse(oNode.valid(True), 'True is a valid time')
		self.assertFalse(oNode.valid(2), '2 is a valid time')
		self.assertFalse(oNode.valid(1.2), '1.2 is a valid time')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid time')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid time')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid time')
		self.assertFalse(oNode.valid([]), '[] is a valid time')
		self.assertFalse(oNode.valid({}), '{} is a valid time')

		# Create a new basic timestamp Node module
		oNode	 = define.Node({
			'__type__':	'timestamp'
		})

		# Check for True
		self.assertTrue(oNode.valid(1), '1 is not a valid timestamp')
		self.assertTrue(oNode.valid(0), '0 is not a valid timestamp')

		# Check for False
		self.assertFalse(oNode.valid(-1), '-1 is a valid timestamp')
		self.assertFalse(oNode.valid('-1'), '"-1" is a valid timestamp')

		# Create a new basic unsigned int Node module
		oNode	 = define.Node({
			'__type__':	'uint'
		})

		# Check for True
		self.assertTrue(oNode.valid(1), '1 is not a valid unsigned int')
		self.assertTrue(oNode.valid(0), '0 is not a valid unsigned int')

		# Check for False
		self.assertFalse(oNode.valid(-1), '-1 is a valid unsigned int')
		self.assertFalse(oNode.valid('-1'), '"-1" is a valid unsigned int')

		# Create a new basic uuid Node module
		oNode	 = define.Node({
			'__type__':	'uuid'
		})

		# Check for True
		self.assertTrue(oNode.valid('52cd4b20-ca32-4433-9516-0c8684ec57c2'), '"52cd4b20-ca32-4433-9516-0c8684ec57c2" is not a valid uuid')
		self.assertTrue(oNode.valid('3b44c5ed-0fea-4478-9f1b-939ae6ec0721'), '"3b44c5ed-0fea-4478-9f1b-939ae6ec0721" is not a valid uuid')
		self.assertTrue(oNode.valid('6432b16a-7e27-47cd-8360-82d82ac70078'), '"6432b16a-7e27-47cd-8360-82d82ac70078" is not a valid uuid')

		# Check for False
		self.assertFalse(oNode.valid('Hello'), '"Hello" is a valid uuid')
		self.assertFalse(oNode.valid(True), '"Hello" is a valid uuid')
		self.assertFalse(oNode.valid(0), '0 is a valid uuid')
		self.assertFalse(oNode.valid(0.1), '0.1 is a valid uuid')
		self.assertFalse(oNode.valid('192.168.0.1'), '"192.168.0.1" is a valid uuid')
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is a valid uuid')
		self.assertFalse(oNode.valid('13:50:00'), '"13:50:00" is a valid uuid')
		self.assertFalse(oNode.valid('2016-03-05 13:50:00'), '"2016-03-05 13:50:00" is a valid uuid')
		self.assertFalse(oNode.valid([]), '[] is a valid uuid')
		self.assertFalse(oNode.valid({}), '{} is a valid uuid')

	def test_Node_Valid_MinMax(self):

		# Create a new minmax date Node module
		oNode	 = define.Node({
			'__type__':		'date',
			'__minimum__':	'2016-01-01',
			'__maximum__':	'2016-12-31'
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-01-01'), '"2016-01-01" is not between "2016-01-01" and "2016-12-31"')
		self.assertTrue(oNode.valid('2016-05-02'), '"2016-05-02" is not between "2016-01-01" and "2016-12-31"')
		self.assertTrue(oNode.valid('2016-10-05'), '"2016-10-05" is not between "2016-01-01" and "2016-12-31"')
		self.assertTrue(oNode.valid('2016-12-31'), '"2016-12-31" is not between "2016-01-01" and "2016-12-31"')

		# Check for False
		self.assertFalse(oNode.valid('2015-12-31'), '"2015-12-31" is between "2016-01-01" and "2016-12-31"')
		self.assertFalse(oNode.valid('2017-01-01'), '"2017-01-01" is between "2016-01-01" and "2016-12-31"')
		self.assertFalse(oNode.valid('3010-01-01'), '"3010-01-01" is between "2016-01-01" and "2016-12-31"')
		self.assertFalse(oNode.valid('1970-01-01'), '"1970-01-01" is between "2016-01-01" and "2016-12-31"')

		# Create a new minmax datetime Node module
		oNode	 = define.Node({
			'__type__':		'datetime',
			'__minimum__':	'2016-01-01 10:00:00',
			'__maximum__':	'2016-12-31 12:00:00'
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-01-01 12:00:00'), '"2016-01-01 12:00:00" is not between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')
		self.assertTrue(oNode.valid('2016-05-02 12:23:34'), '"2016-05-02 12:23:34" is not between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')
		self.assertTrue(oNode.valid('2016-10-05 09:12:23'), '"2016-10-05 09:12:23" is not between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')
		self.assertTrue(oNode.valid('2016-12-31 10:00:00'), '"2016-12-31 10:00:00" is not between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')

		# Check for False
		self.assertFalse(oNode.valid('2016-12-31 12:00:01'), '"2015-12-31 12:00:01" is between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')
		self.assertFalse(oNode.valid('2017-01-01 00:00:00'), '"2017-01-01 00:00:00" is between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')
		self.assertFalse(oNode.valid('3010-01-01 00:00:00'), '"3010-01-01 00:00:00" is between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')
		self.assertFalse(oNode.valid('2016-01-01 09:59:59'), '"1970-01-01 09:59:59" is between "2016-01-01 10:00:00" and "2016-12-31 12:00:00"')

		# Create a new minmax decimal Node module
		oNode	 = define.Node({
			'__type__':		'decimal',
			'__minimum__':	Decimal('-10.0'),
			'__maximum__':	Decimal('10.0')
		})

		# Check for True
		self.assertTrue(oNode.valid(Decimal('-10')), '-10 is not between -10.0 and 10.0')
		self.assertTrue(oNode.valid(Decimal('-5.61')), '-5.61 is not between -10.0 and 10.0')
		self.assertTrue(oNode.valid(Decimal('0.1')), '0.1 is not between -10.0 and 10.0')
		self.assertTrue(oNode.valid(Decimal('6.20982')), '6.20982 is not between -10.0 and 10.0')

		# Check for False
		self.assertFalse(oNode.valid(Decimal('-10.00001')), '-10.00001 is between -10.0 and 10.0')
		self.assertFalse(oNode.valid(Decimal('-2000.01')), '-2000.01 is between -10.0 and 10.0')
		self.assertFalse(oNode.valid(Decimal('13.314')), '13 is between -10.0 and 10.0')
		self.assertFalse(oNode.valid(Decimal('11')), '11 is between -10.0 and 10.0')

		# Create a new minmax int Node module
		oNode	 = define.Node({
			'__type__':		'int',
			'__minimum__':	'-10',
			'__maximum__':	10
		})

		# Check for True
		self.assertTrue(oNode.valid(-10), '-10 is not between -10 and 10')
		self.assertTrue(oNode.valid(-5), '-5 is not between -10 and 10')
		self.assertTrue(oNode.valid(0), '0 is not between -10 and 10')
		self.assertTrue(oNode.valid(6), '6 is not between -10 and 10')

		# Check for False
		self.assertFalse(oNode.valid(-11), '-11 is between -10 and 10')
		self.assertFalse(oNode.valid(-2000), '-2000 is between -10 and 10')
		self.assertFalse(oNode.valid(13), '13 is between -10 and 10')
		self.assertFalse(oNode.valid(11), '11 is between -10 and 10')

		# Create a new minmax ip Node module
		oNode	 = define.Node({
			'__type__':		'ip',
			'__minimum__':	'192.168.0.1',
			'__maximum__':	'192.168.1.1'
		})

		# Check for True
		self.assertTrue(oNode.valid('192.168.1.0'), '"192.168.1.0" is not between "192.168.0.1" and "192.168.1.1"')
		self.assertTrue(oNode.valid('192.168.0.1'), '"192.168.0.1" is not between "192.168.0.1" and "192.168.1.1"')
		self.assertTrue(oNode.valid('192.168.1.1'), '"192.168.1.1" is not between "192.168.0.1" and "192.168.1.1"')
		self.assertTrue(oNode.valid('192.168.0.246'), '"192.168.0.246" is not between "192.168.0.1" and "192.168.1.1"')
		self.assertTrue(oNode.valid('192.168.0.13'), '"192.168.0.13" is not between "192.168.0.1" and "192.168.1.1"')

		# Check for False
		self.assertFalse(oNode.valid('192.169.0.1'), '"192.169.0.1" is between "192.168.0.1" and "192.168.1.1"')
		self.assertFalse(oNode.valid('193.168.0.1'), '"193.168.0.1" is between "192.168.0.1" and "192.168.1.1"')
		self.assertFalse(oNode.valid('192.0.0.1'), '"192.0.0.1" is between "192.168.0.1" and "192.168.1.1"')

		# Create a new minmax string Node module
		oNode	 = define.Node({
			'__type__':		'string',
			'__minimum__':	3,
			'__maximum__':	12
		})

		# Check for True
		self.assertTrue(oNode.valid('hello'), 'the length of "hello" is not between 3 and 12 characters')
		self.assertTrue(oNode.valid('1234'), 'the length of "1234" is not between 3 and 12 characters')
		self.assertTrue(oNode.valid('Wonderful'), 'the length of "Wonderful" is not between 3 and 12 characters')
		self.assertTrue(oNode.valid('            '), 'the length of "			" is not between 3 and 12 characters')

		# Check for False
		self.assertFalse(oNode.valid(''), 'the length of "" is between 3 and 12 characters')
		self.assertFalse(oNode.valid('me'), 'the length of "me" is between 3 and 12 characters')
		self.assertFalse(oNode.valid('Hello, World!'), 'the length of "Hello, World!" is between 3 and 12 characters')
		self.assertFalse(oNode.valid('             '), 'the length of "			 " is between 3 and 12 characters')


		# Create a new minmax time Node module
		oNode	 = define.Node({
			'__type__':		'time',
			'__minimum__':	'10:00:00',
			'__maximum__':	'12:00:00'
		})

		# Check for True
		self.assertTrue(oNode.valid('12:00:00'), '"12:00:00" is not between "10:00:00" and "12:00:00"')
		self.assertTrue(oNode.valid('11:23:34'), '"11:23:34" is not between "10:00:00" and "12:00:00"')
		self.assertTrue(oNode.valid('10:12:23'), '"10:12:23" is not between "10:00:00" and "12:00:00"')
		self.assertTrue(oNode.valid('10:00:00'), '"10:00:00" is not between "10:00:00" and "12:00:00"')

		# Check for False
		self.assertFalse(oNode.valid('12:00:01'), '"12:00:01" is between "10:00:00" and "12:00:00"')
		self.assertFalse(oNode.valid('00:00:00'), '"00:00:00" is between "10:00:00" and "12:00:00"')
		self.assertFalse(oNode.valid('23:59:59'), '"23:59:59" is between "10:00:00" and "12:00:00"')
		self.assertFalse(oNode.valid('09:59:59'), '"09:59:59" is between "10:00:00" and "12:00:00"')

		# Create a new minmax timestamp Node module
		oNode	 = define.Node({
			'__type__':		'timestamp',
			'__minimum__':	'10',
			'__maximum__':	10000
		})

		# Check for True
		self.assertTrue(oNode.valid(10), '10 is not between 10 and 10000')
		self.assertTrue(oNode.valid(100), '100 is not between 10 and 10000')
		self.assertTrue(oNode.valid(1000), '1000 is not between 10 and 10000')
		self.assertTrue(oNode.valid(9999), '9999 is not between 10 and 10000')

		# Check for False
		self.assertFalse(oNode.valid(-11), '-11 is between 10 and 10000')
		self.assertFalse(oNode.valid(-2000), '-2000 is between 10 and 10000')
		self.assertFalse(oNode.valid(10013), '10013 is between 10 and 10000')
		self.assertFalse(oNode.valid(9), '9 is between 10 and 10000')

		# Create a new minmax uint Node module
		oNode	 = define.Node({
			'__type__':		'uint',
			'__minimum__':	'10',
			'__maximum__':	10000
		})

		# Check for True
		self.assertTrue(oNode.valid(10), '10 is not between 10 and 10000')
		self.assertTrue(oNode.valid(100), '100 is not between 10 and 10000')
		self.assertTrue(oNode.valid(1000), '1000 is not between 10 and 10000')
		self.assertTrue(oNode.valid(9999), '9999 is not between 10 and 10000')

		# Check for False
		self.assertFalse(oNode.valid(-11), '-11 is between 10 and 10000')
		self.assertFalse(oNode.valid(-2000), '-2000 is between 10 and 10000')
		self.assertFalse(oNode.valid(10013), '10013 is between 10 and 10000')
		self.assertFalse(oNode.valid(9), '9 is between 10 and 10000')

	def test_Node_Valid_Options(self):

		# Create a new basic base64 Node module
		oNode = define.Node({
			'__type__': 'base64',
			'__options__': ['SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==', 'WW8gWW8gWW8=', 'RG92ZXRhaWwgaXMgdGhlIHNoaXQu']
		})

		# Check for True
		self.assertTrue(oNode.valid('SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ=='), '"SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==" is not in ["SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==", "WW8gWW8gWW8=", "RG92ZXRhaWwgaXMgdGhlIHNoaXQu"]')
		self.assertTrue(oNode.valid('WW8gWW8gWW8='), '"WW8gWW8gWW8=" is not in ["SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==", "WW8gWW8gWW8=", "RG92ZXRhaWwgaXMgdGhlIHNoaXQu"]')
		self.assertTrue(oNode.valid('RG92ZXRhaWwgaXMgdGhlIHNoaXQu'), '"RG92ZXRhaWwgaXMgdGhlIHNoaXQu" is not in ["SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==", "WW8gWW8gWW8=", "RG92ZXRhaWwgaXMgdGhlIHNoaXQu"]')

		# Check for False
		self.assertFalse(oNode.valid('SPVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ=='), '"SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==" is in ["SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==", "WW8gWW8gWW8=", "RG92ZXRhaWwgaXMgdGhlIHNoaXQu"]')
		self.assertFalse(oNode.valid('WW8gWW8gWW8==='), '"WW8gWW8gWW8===" is in ["SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==", "WW8gWW8gWW8=", "RG92ZXRhaWwgaXMgdGhlIHNoaXQu"]')
		self.assertFalse(oNode.valid('RG92ZXRhaWwgaXMgdGhlIHNo'), '"RG92ZXRhaWwgaXMgdGhlIHNo" is in ["SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IQ==", "WW8gWW8gWW8=", "RG92ZXRhaWwgaXMgdGhlIHNoaXQu"]')

		# Create a new options date Node module
		oNode	 = define.Node({
			'__type__':		'date',
			'__options__':	['2016-03-06', '2016-03-07', '2016-03-08']
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-03-06'), '"2016-03-06" is not in ["2016-03-06", "2016-03-07", "2016-03-08"]')
		self.assertTrue(oNode.valid('2016-03-07'), '"2016-03-07" is not in ["2016-03-06", "2016-03-07", "2016-03-08"]')
		self.assertTrue(oNode.valid('2016-03-08'), '"2016-03-08" is not in ["2016-03-06", "2016-03-07", "2016-03-08"]')

		# Check for True
		self.assertFalse(oNode.valid('2016-03-05'), '"2016-03-05" is in ["2016-03-06", "2016-03-07", "2016-03-08"]')
		self.assertFalse(oNode.valid('2016-03-09'), '"2016-03-09" is in ["2016-03-06", "2016-03-07", "2016-03-08"]')
		self.assertFalse(oNode.valid('2015-03-07'), '"2015-03-07" is in ["2016-03-06", "2016-03-07", "2016-03-08"]')

		# Create a new options datetime Node module
		oNode	 = define.Node({
			'__type__':		'datetime',
			'__options__':	['2016-03-06 02:00:00', '2016-03-07 00:02:00', '2016-03-08 00:00:02']
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-03-06 02:00:00'), '"2016-03-06 02:00:00" is not in ["2016-03-06 02:00:00", "2016-03-07 00:02:00", "2016-03-08 00:00:02"]')
		self.assertTrue(oNode.valid('2016-03-07 00:02:00'), '"2016-03-07 00:02:00" is not in ["2016-03-06 02:00:00", "2016-03-07 00:02:00", "2016-03-08 00:00:02"]')
		self.assertTrue(oNode.valid('2016-03-08 00:00:02'), '"2016-03-08 00:00:02" is not in ["2016-03-06 02:00:00", "2016-03-07 00:02:00", "2016-03-08 00:00:02"]')

		# Check for True
		self.assertFalse(oNode.valid('2016-03-05 02:00:00'), '"2016-03-05 02:00:00" is in ["2016-03-06 02:00:00", "2016-03-07 00:02:00", "2016-03-08 00:00:02"]')
		self.assertFalse(oNode.valid('2016-03-09 00:02:00'), '"2016-03-09 00:02:00" is in ["2016-03-06 02:00:00", "2016-03-07 00:02:00", "2016-03-08 00:00:02"]')
		self.assertFalse(oNode.valid('2015-03-07 00:00:02'), '"2015-03-07 00:00:02" is in ["2016-03-06 02:00:00", "2016-03-07 00:02:00", "2016-03-08 00:00:02"]')

		# Create a new options decimal Node module
		oNode	 = define.Node({
			'__type__':		'decimal',
			'__options__':	[Decimal('0.0'), Decimal('2.0'), Decimal('123.345'), Decimal('0.6')]
		})

		# Check for True
		self.assertTrue(oNode.valid(Decimal('0.0')), '0.0 is not in [0.0, 2.0, 123.345, 0.6]')
		self.assertTrue(oNode.valid(Decimal('2.0')), '2.0 is not in [0.0, 2.0, 123.345, 0.6]')
		self.assertTrue(oNode.valid(Decimal('123.345')), '123.345 is not in [0.0, 2.0, 123.345, 0.6]')
		self.assertTrue(oNode.valid(Decimal('0.6')), ' is not in [0.0, 2.0, 123.345, 0.6]')

		# Check for False
		self.assertFalse(oNode.valid(Decimal('1')), '0 is in [0.0, 2.0, 123.345, 0.6]')
		self.assertFalse(oNode.valid(Decimal('2.1')), '2.1 is in [0.0, 2.0, 123.345, 0.6]')
		self.assertFalse(oNode.valid(Decimal('123.45')), '123.45 is in [0.0, 2.0, 123.345, 0.6]')
		self.assertFalse(oNode.valid(Decimal('0.06')), '0.06 is in [0.0, 2.0, 123.345, 0.6]')

		# Create a new options int Node module
		oNode	 = define.Node({
			'__type__':		'int',
			'__options__':	[-1, 0, 2, 4]
		})

		# Check for True
		self.assertTrue(oNode.valid(-1), '-1 is not in [-1, 0, 2, 4]')
		self.assertTrue(oNode.valid(0), '0 is not in [-1, 0, 2, 4]')
		self.assertTrue(oNode.valid(2), '2 is not in [-1, 0, 2, 4]')
		self.assertTrue(oNode.valid(4), '4 is not in [-1, 0, 2, 4]')

		# Check for False
		self.assertFalse(oNode.valid(1), '1 is in [-1, 0, 2, 4]')
		self.assertFalse(oNode.valid(-2), '-2 is in [-1, 0, 2, 4]')
		self.assertFalse(oNode.valid(3), '3 is in [-1, 0, 2, 4]')
		self.assertFalse(oNode.valid(-100), '-100 is in [-1, 0, 2, 4]')

		# Create a new options ip Node module
		oNode	 = define.Node({
			'__type__':		'ip',
			'__options__':	['10.0.0.1', '192.168.0.1', '127.0.0.1']
		})

		# Check for True
		self.assertTrue(oNode.valid('10.0.0.1'), '"10.0.0.1" is not in ["10.0.0.1", "192.168.0.1", "127.0.0.1"]')
		self.assertTrue(oNode.valid('192.168.0.1'), '"192.168.0.1" is not in ["10.0.0.1", "192.168.0.1", "127.0.0.1"]')
		self.assertTrue(oNode.valid('127.0.0.1'), '"127.0.0.1" is not in ["10.0.0.1", "192.168.0.1", "127.0.0.1"]')

		# Check for False
		self.assertFalse(oNode.valid('11.0.0.1'), '"11.0.0.1" is in ["10.0.0.1", "192.168.0.1", "127.0.0.1"]')
		self.assertFalse(oNode.valid('192.169.1.1'), '"192.169.1.1" is in ["10.0.0.1", "192.168.0.1", "127.0.0.1"]')
		self.assertFalse(oNode.valid('0.0.0.0'), '"0.0.0.0" is in ["10.0.0.1", "192.168.0.1", "127.0.0.1"]')

		# Create a new options md5 Node module
		oNode	 = define.Node({
			'__type__':		'md5',
			'__options__':	['7b967af699a0a18b1f2bdc9704537a3e', '889ffd8cc409445187c4258d138192b6', '49c0d2aef0ab2634b0051544cdbf2415']
		})

		# Check for True
		self.assertTrue(oNode.valid('7b967af699a0a18b1f2bdc9704537a3e'), '"7b967af699a0a18b1f2bdc9704537a3e" is not in ["7b967af699a0a18b1f2bdc9704537a3e", "889ffd8cc409445187c4258d138192b6", "49c0d2aef0ab2634b0051544cdbf2415"]')
		self.assertTrue(oNode.valid('889ffd8cc409445187c4258d138192b6'), '"889ffd8cc409445187c4258d138192b6" is not in ["7b967af699a0a18b1f2bdc9704537a3e", "889ffd8cc409445187c4258d138192b6", "49c0d2aef0ab2634b0051544cdbf2415"]')
		self.assertTrue(oNode.valid('49c0d2aef0ab2634b0051544cdbf2415'), '"49c0d2aef0ab2634b0051544cdbf2415" is not in ["7b967af699a0a18b1f2bdc9704537a3e", "889ffd8cc409445187c4258d138192b6", "49c0d2aef0ab2634b0051544cdbf2415"]')

		# Check for False
		self.assertFalse(oNode.valid('49c0d2aef0ab2634b1051544cdbf2415'), '"49c0d2aef0ab2634b1051544cdbf2415" is in ["7b967af699a0a18b1f2bdc9704537a3e", "889ffd8cc409445187c4258d138192b6", "49c0d2aef0ab2634b0051544cdbf2415"]')
		self.assertFalse(oNode.valid('889ffd8cc409445287c4258d138192b6'), '"889ffd8cc409445287c4258d138192b6" is in ["7b967af699a0a18b1f2bdc9704537a3e", "889ffd8cc409445187c4258d138192b6", "49c0d2aef0ab2634b0051544cdbf2415"]')
		self.assertFalse(oNode.valid('49c0d2aee0ab2634b0051544cdbf2415'), '"49c0d2aee0ab2634b0051544cdbf2415" is in ["7b967af699a0a18b1f2bdc9704537a3e", "889ffd8cc409445187c4258d138192b6", "49c0d2aef0ab2634b0051544cdbf2415"]')

		# Create a new options string Node module
		oNode	 = define.Node({
			'__type__':		'string',
			'__options__':	['hello', 'there', 'my', '00000']
		})

		# Check for True
		self.assertTrue(oNode.valid('hello'), '"hello" is not in ["hello", "there", "my", "00000"]')
		self.assertTrue(oNode.valid('there'), '"there" is not in ["hello", "there", "my", "00000"]')
		self.assertTrue(oNode.valid('my'), '"my" is not in ["hello", "there", "my", "00000"]')
		self.assertTrue(oNode.valid('00000'), '"00000" is not in ["hello", "there", "my", "00000"]')

		# Check for False
		self.assertFalse(oNode.valid('49c0d2aef0ab2634b1051544cdbf2415'), '"49c0d2aef0ab2634b1051544cdbf2415" is in ["hello", "there", "my", "00000"]')
		self.assertFalse(oNode.valid('889ffd8cc409445287c4258d138192b6'), '"889ffd8cc409445287c4258d138192b6" is in ["hello", "there", "my", "00000"]')
		self.assertFalse(oNode.valid('49c0d2aee0ab2634b0051544cdbf2415'), '"49c0d2aee0ab2634b0051544cdbf2415" is in ["hello", "there", "my", "00000"]')
		self.assertFalse(oNode.valid('0000'), '"00000" is in ["hello", "there", "my", "00000"]')

		# Create a new options time Node module
		oNode	 = define.Node({
			'__type__':		'time',
			'__options__':	['12:00:12', '00:00:00', '12:23:00']
		})

		# Check for True
		self.assertTrue(oNode.valid('12:00:12'), '"12:00:12" is not in ["12:00:12", "00:00:00", "12:23:00"]')
		self.assertTrue(oNode.valid('00:00:00'), '"00:00:00" is not in ["12:00:12", "00:00:00", "12:23:00"]')
		self.assertTrue(oNode.valid('12:23:00'), '"12:23:00" is not in ["12:00:12", "00:00:00", "12:23:00"]')

		# Check for True
		self.assertFalse(oNode.valid('00:12:00'), '"00:12:00" is in ["12:00:12", "00:00:00", "12:23:00"]')
		self.assertFalse(oNode.valid('23:59:59'), '"23:59:59" is in ["12:00:12", "00:00:00", "12:23:00"]')
		self.assertFalse(oNode.valid('00:12:23'), '"00:12:23" is in ["12:00:12", "00:00:00", "12:23:00"]')

		# Create a new options timestamp Node module
		oNode	 = define.Node({
			'__type__':		'timestamp',
			'__options__':	[0, 1, 2, 3]
		})

		# Check for True
		self.assertTrue(oNode.valid(0), '0 is not in [0, 1, 2, 3]')
		self.assertTrue(oNode.valid(1), '1 is not in [0, 1, 2, 3]')
		self.assertTrue(oNode.valid(2), '2 is not in [0, 1, 2, 3]')
		self.assertTrue(oNode.valid(3), '3 is not in [0, 1, 2, 3]')

		# Check for False
		self.assertFalse(oNode.valid(4), '4 is in [0, 1, 2, 3]')
		self.assertFalse(oNode.valid(-2), '-2 is in [0, 1, 2, 3]')
		self.assertFalse(oNode.valid(10000), '10000 is in [0, 1, 2, 3]')
		self.assertFalse(oNode.valid(-100), '-100 is in [0, 1, 2, 3]')

		# Create a new options uint Node module
		oNode	 = define.Node({
			'__type__':		'uint',
			'__options__':	[0, 1, 2, 3]
		})

		# Check for True
		self.assertTrue(oNode.valid(0), '0 is not in [0, 1, 2, 3]')
		self.assertTrue(oNode.valid(1), '1 is not in [0, 1, 2, 3]')
		self.assertTrue(oNode.valid(2), '2 is not in [0, 1, 2, 3]')
		self.assertTrue(oNode.valid(3), '3 is not in [0, 1, 2, 3]')

		# Check for False
		self.assertFalse(oNode.valid(4), '4 is in [0, 1, 2, 3]')
		self.assertFalse(oNode.valid(-2), '-2 is in [0, 1, 2, 3]')
		self.assertFalse(oNode.valid(10000), '10000 is in [0, 1, 2, 3]')
		self.assertFalse(oNode.valid(-100), '-100 is in [0, 1, 2, 3]')

	def test_Node_Valid_Regex(self):

		# Create a new options any Node module
		oNode	 = define.Node({
			'__type__':		'string',
			'__regex__':	r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'
		})

		# Check for True
		self.assertTrue(oNode.valid('2016-03-05'), '"2016-03-05" is not in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertTrue(oNode.valid('2020-12-25'), '"2020-12-25" is not in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertTrue(oNode.valid('1970-01-01'), '"1970-01-01" is not in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')

		# Check for False
		self.assertFalse(oNode.valid('70-01-01'), '"70-01-01" is in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertFalse(oNode.valid('10000-01-01'), '"10000-01-01" is in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertFalse(oNode.valid('1970-00-01'), '"1970-00-01" is in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertFalse(oNode.valid('2000-12-00'), '"2000-12-00" is in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertFalse(oNode.valid('2000-12-32'), '"2000-12-32" is in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')
		self.assertFalse(oNode.valid('2000-13-10'), '"2000-13-10" is in /^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$/')

		# Create a new options any Node module
		oNode	 = define.Node({
			'__type__':		'string',
			'__regex__':	r'^(?:hello|there|my|friend)$'
		})

		# Check for True
		self.assertTrue(oNode.valid('hello'), '"hello" is not in /^(?:hello|there|my|friend)$/')
		self.assertTrue(oNode.valid('there'), '"there" is not in /^(?:hello|there|my|friend)$/')
		self.assertTrue(oNode.valid('my'), '"my" is not in /^(?:hello|there|my|friend)$/')
		self.assertTrue(oNode.valid('friend'), '"friend" is not in /^(?:hello|there|my|friend)$/')

		# Check for False
		self.assertFalse(oNode.valid('suck it'), '"suck it" is in /^(?:hello|there|my|friend)$/')
		self.assertFalse(oNode.valid('HELLO'), '"HELLO" is in /^(?:hello|there|my|friend)$/')
		self.assertFalse(oNode.valid('WhatWhat'), '"WhatWhat" is in /^(?:hello|there|my|friend)$/')
		self.assertFalse(oNode.valid('2309 r gjvhjw0e9f'), '"2309 r gjvhjw0e9f" is in /^(?:hello|there|my|friend)$/')

	def test_Option_Clean(self):

		oOption	= define.Options([
			{"__type__":"uint"},
			{"__type__":"string","__options__":["hello", "there"]}
		])

		self.assertTrue(oOption.clean(0) == 0, '0 does not equal 0')
		self.assertTrue(oOption.clean('0') == 0, '"0" does not equal 0')
		self.assertTrue(oOption.clean(1) == 1, '1 does not equal 1')
		self.assertTrue(oOption.clean('1') == 1, '"1" does not equal 1')
		self.assertTrue(oOption.clean('hello') == 'hello', '"hello" does not equal "hello"')
		self.assertTrue(oOption.clean('there') == 'there', '"hello" does not equal "there"')

	def test_Option_Iterate(self):

		l = [
			{"__type__":"uint"},
			{"__type__":"string","__options__":["hello", "there"]}
		]

		oOption	= define.Options([
			{"__type__":"uint"},
			{"__type__":"string","__options__":["hello", "there"]}
		])

		self.assertTrue(len(oOption) == 2, 'Length is not 2');

		iTest = 0
		for i in range(len(oOption)):
			self.assertTrue(i == iTest, '%d is not %d' % (i, iTest))
			iTest += 1

		iTest = 0
		for d in oOption:
			self.assertTrue(d.to_dict() == l[iTest], 'structure doesn\'t match')
			iTest += 1

		self.assertTrue(oOption[0].to_dict() == {"__type__":"uint"}, 'structure doesn\'t match')
		self.assertTrue(oOption[1].to_dict() == {"__type__":"string","__options__":["hello", "there"]}, 'structure doesn\'t match')

	def test_Option_Valid(self):

		oOption	= define.Options([
			{"__type__":"uint"},
			{"__type__":"string","__options__":["hello", "there"]}
		])

		# Test for true
		self.assertTrue(oOption.valid(0), '0 does not equal 0')
		self.assertTrue(oOption.valid('0'), '"0" does not equal 0')
		self.assertTrue(oOption.valid(1), '1 does not equal 1')
		self.assertTrue(oOption.valid('1'), '"1" does not equal 1')
		self.assertTrue(oOption.valid('hello'), '"hello" does not equal "hello"')
		self.assertTrue(oOption.valid('there'), '"hello" does not equal "there"')

		# Test for false
		self.assertFalse(oOption.valid(-1), '-1 is a valid option')
		self.assertFalse(oOption.valid('-1'), '"-1" is a valid option')
		self.assertFalse(oOption.valid('something'), '"something" is a valid option')
		self.assertFalse(oOption.valid('else'), '"else" is a valid option')

	def test_Tree_to_json(self):

		o	= define.Tree({"__name__":"hello","field1":{"__type__":"uint"},"field2":{"field2_1":{"__type__":"string","__regex__":"^\\S+$"},"field2_2":{"__type__":"uint","__options__":[0,1,2,34]}},"field3":{"__array__":"unique","__type__":"decimal"},"field4":{"__array__":"duplicates","__ui__":{"ui":"information"},"field4_1":{"__type__":"md5"},"field4_2":{"field4_2_1":{"__type__":"date","__mysql__":"MySQL information"}}}})

		# It is next to impossible to compare JSON output between python2 and
		#	python3, so instead generate dicts from the JSON and compare those
		d1 = json.loads(o.to_json())
		d2 = json.loads('{"field2": {"field2_2": {"__options__": [0, 1, 2, 34], "__type__": "uint"}, "field2_1": {"__regex__": "^\\\\S+$", "__type__": "string"}}, "__name__": "hello", "field1": {"__type__": "uint"}, "field4": {"__ui__": {"ui": "information"}, "field4_1": {"__type__": "md5"}, "__array__": "duplicates", "field4_2": {"field4_2_1": {"__type__": "date", "__mysql__": "MySQL information"}}}, "field3": {"__type__": "decimal", "__array__": "unique"}}')
		self.assertTrue(d1 == d2, 'to_json failed: %s' % o.to_json())

	def test_Tree_Valid(self):

		# Build a Tree
		o	= define.Tree({"__name__":"hello","field1":{"__type__":"uint"},"field2":{"field2_1":{"__type__":"string","__regex__":"^\\S+$"},"field2_2":{"__type__":"uint","__options__":[0,1,2,34]}},"field3":{"__array__":"unique","__type__":"decimal"},"field4":{"__array__":"duplicates","field4_1":{"__type__":"md5"},"field4_2":{"field4_2_1":{"__type__":"date"}}}})

		# Check for True
		self.assertTrue(o['field2']['field2_1'].valid('Hello'), '"Hello" is not a valid value for hello.field2.field2_1')
		self.assertTrue(o['field2'].valid({"field2_1":"Hello","field2_2":34}), '{"field2_1":"Hello","field2_2":34} is not a valid value for hello.field2')
		self.assertTrue(o.valid({"field1":2,"field2":{"field2_1":"ThisString","field2_2":34},"field3":[0.3,10.3,20.3],"field4":[{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"},},{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"}}]}), '{"field1":2,"field2":{"field2_1":"ThisString","field2_2":34},"field3":[0.3,10.3,20.3],"field4":[{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"},},{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"}}]} is not a valid value for hello')

		# Check for False
		self.assertFalse(o['field2']['field2_1'].valid('    '), '"    " is not a valid value for hello.field2.field2_1')
		self.assertTrue(o['field2']['field2_1'].validation_failures[0][0] == '', 'error name is not correct: "' + str(o['field2']['field2_1'].validation_failures[0][0]) + '"')
		self.assertTrue(o['field2']['field2_1'].validation_failures[0][1] == 'failed regex (custom)', 'error value is not correct')

		self.assertFalse(o['field2'].valid({"field2_1":"Hello","field2_2":4}), '{"field2_1":"Hello","field2_2":4} is not a valid value for hello.field2')
		self.assertTrue(o['field2'].validation_failures[0][0] == 'field2_2', 'error name is not correct: "' + str(o['field2'].validation_failures[0][0]) + '"')
		self.assertTrue(o['field2'].validation_failures[0][1] == 'not in options', 'error value is not correct: "' + str(o['field2'].validation_failures[0][1]) + '"')

		self.assertFalse(o['field2'].valid({"field2_1":"   ","field2_2":2}), '{"field2_1":"   ","field2_2":2} is not a valid value for hello.field2')
		self.assertTrue(o['field2'].validation_failures[0][0] == 'field2_1', 'error name is not correct: "' + str(o['field2'].validation_failures[0][0]) + '"')
		self.assertTrue(o['field2'].validation_failures[0][1] == 'failed regex (custom)', 'error value is not correct: "' + str(o['field2'].validation_failures[0][1]) + '"')

		self.assertFalse(o.valid({"field1":"NotAnINTEGER","field2":{"field2_1":"ThisString","field2_2":34},"field3":[0.3,10.3,20.3],"field4":[{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"},},{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"}}]}), '{"field1":"NotAnINTEGER","field2":{"field2_1":"ThisString","field2_2":34},"field3":[0.3,10.3,20.3],"field4":[{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"},},{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"}}]} is not a valid value for hello')
		self.assertTrue(o.validation_failures[0][0] == 'hello.field1', 'error name is not correct: "' + str(o.validation_failures[0][0]) + '"')
		self.assertTrue(o.validation_failures[0][1] == 'not an integer', 'error value is not correct: "' + str(o.validation_failures[0][1]) + '"')

		self.assertFalse(o.valid({"field1":"NotAnINTEGER","field2":{"field2_1":"This String","field2_2":3},"field3":[0.3,10.3,20.3],"field4":[{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"},},{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"}}]}, False), '{"field1":"NotAnINTEGER","field2":{"field2_1":"ThisString","field2_2":34},"field3":[0.3,10.3,20.3],"field4":[{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"},},{"field4_1":"49c0d2aef0ab2634b0051544cdbf2415","field4_2":{"field4_2_1":"2016-03-05"}}]} is not a valid value for hello')

		# Pythons complete lack of keeping keys in the same order as they were
		#	added results in some inconsistent error messages, so we need to
		#	hack the test results a tad
		for err in o.validation_failures:
			if err[0] == 'field1' and err[1] == 'not an integer':
				break
		else:
			self.assertTrue(False, 'field1 error not found in list: %s' % str(o.validation_failures))

		for err in o.validation_failures:
			if err[0] == 'field2.field2_1' and err[1] == 'failed regex (custom)':
				break
		else:
			self.assertTrue(False, 'field2.field2_1 error not found in list: %s' % str(o.validation_failures))

		for err in o.validation_failures:
			if err[0] == 'field2.field2_2' and err[1] == 'not in options':
				break
		else:
			self.assertTrue(False, 'field2.field2_2 error not found in list: %s' % str(o.validation_failures))

	def test_Tree_Valid_Requires(self):

		# Build a complex tree with requires
		o	= define.Tree({"__name__":"test","__requires__":{"field2":"field1"},"field1":{"__type__":"uint"},"field2":{"__type__":"uint"}})

	def test_Hash_Clean(self):

		o = define.Hash({"__type__":"price", "__hash__":{"__type__":"string", "__regex__":"^\\\d+$"}})

		self.assertTrue(o.clean({"12345":99.99,"54321":66.66,"98765":"123"}) == {"12345":"99.99","54321":"66.66","98765":"123.00"}, "hash isn't cleaned")

	def test_Hash_Valid(self):

		o = define.Hash({"__type__":"price", "__hash__":"uuid"})

		self.assertTrue(o.valid({
			"52cd4b20-ca32-4433-9516-0c8684ec57c2" : 99.99,
			"3b44c5ed-0fea-4478-9f1b-939ae6ec0721" : 66.66
		}), 'Hash is not valid')
