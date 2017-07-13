import codecs
from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
    ],
}


TESTS_REQUIRE = [
    'pyhamcrest'
    'nti.testing',
    'zope.testing',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.namedfile',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI NamedFile support",
    long_description=(_read('README.rst') + '\n\n' + _read("CHANGES.rst")),
    license='Apache',
    keywords='NTI named file support',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nti.base',
        'nti.externalization',
        'nti.mimetype',
        'nti.property',
        'nti.schema',
        'plone.namedfile==3.0.9',
        'six',
        'zope.annotation',
        'zope.component',
        'zope.container',
        'zope.deferredimport',
        'zope.file',
        'zope.interface',
        'zope.location',
        'zope.mimetype',
        'zope.schema',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points,
)
