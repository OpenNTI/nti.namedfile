import codecs
from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
    ],
}


TESTS_REQUIRE = [
    'fudge',
    'nti.testing',
    'zope.formlib',
    'zope.dottedname',
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
        'Framework :: Zope3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/NextThought/nti.namedfile",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'awesome-slugify',
        'nti.base',
        'nti.externalization',
        'nti.mimetype',
        'nti.plone.namedfile',
        'nti.property',
        'nti.schema',
        'piexif',
        'Pillow',
        'six',
        'zope.annotation',
        'zope.component',
        'zope.container',
        'zope.deprecation',
        'zope.deferredimport',
        'zope.file',
        'zope.formlib',
        'zope.interface',
        'zope.location',
        'zope.mimetype',
        'zope.schema',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
            'zope.formlib',
        ],
    },
    entry_points=entry_points,
)
