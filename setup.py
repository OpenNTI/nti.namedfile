import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
	'console_scripts': [
	],
}

TESTS_REQUIRE = [
	'nose',
	'nose-timer',
	'nose-pudb',
	'nose-progressive',
	'nose2[coverage_plugin]',
	'pyhamcrest',
	'nti.testing'
]

setup(
	name='nti.namedfile',
	version=VERSION,
	author='Jason Madden',
	author_email='jason@nextthought.com',
	description="NTI NamedFile support",
	long_description=codecs.open('README.rst', encoding='utf-8').read(),
	license='Proprietary',
	keywords='NTI named file support',
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: Implementation :: CPython'
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
	tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
		'plone.namedfile<=3.0.9',
		'zope.annotation',
		'zope.app.file',
		'zope.component',
		'zope.container',
		'zope.deferredimport',
		'zope.interface',
		'zope.location',
		'zope.mimetype',
		'zope.schema',
		'zope.security',
		'nti.common',
		'nti.coremetadata',
		'nti.externalization',
		'nti.schema'
	],
	extras_require={
		'test': TESTS_REQUIRE,
	},
	dependency_links=[],
	entry_points=entry_points
)
