from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='define-oc',
	version='1.0.0',
	description='A system for defining and validating data regardless of data store',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/format-oc',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/format-oc',
		'Source': 'https://github.com/ouroboroscoding/define-python',
		'Tracker': 'https://github.com/ouroboroscoding/define-python/issues'
	},
	keywords=['data','format','database','db','sql','nosql'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['define'],
	python_requires='>=3.10',
	install_requires=[
		"jsonb>=1.0.0,<1.1"
	],
	test_suite='tests',
	zip_safe=True
)