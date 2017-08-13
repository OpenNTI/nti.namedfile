#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.deprecation import deprecated

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedImage as PloneNamedImage
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile
from plone.namedfile.file import NamedBlobImage as PloneNamedBlobImage

from nti.base._compat import text_

from nti.base.interfaces import INamed

from nti.base.mixins import CreatedAndModifiedTimeMixin

from nti.namedfile.interfaces import INamedFile
from nti.namedfile.interfaces import INamedImage
from nti.namedfile.interfaces import INamedBlobFile
from nti.namedfile.interfaces import INamedBlobImage

from nti.property.property import alias
from nti.property.property import read_alias


_nameFinder = re.compile(r'(.*[\\/:])?(.+)')


def name_finder(filename):
    match = _nameFinder.match(filename) if filename else None
    result = match.group(2) if match else None
    return result
nameFinder = name_finder


def get_context_name(context):
    result = None
    if hasattr(context, 'name'):
        result = context.name
    if not result and INamed.providedBy(context):
        result = NamedFileMixin.nameFinder(context.filename) \
              or context.filename
    return result
get_file_name = get_context_name


def safe_filename(s):
    __traceback_info__ = s
    if s:
        try:
            s = s.encode("ascii", 'xmlcharrefreplace')
        except Exception:
            pass
        s = re.sub(r'[/<>:;"\\|#?*\s]+', '_', s)
        s = re.sub(r'&', '_', s)
        try:
            s = text_(s)
        except UnicodeDecodeError:
            s = s.decode('utf-8')
    return s


class NamedFileMixin(CreatedAndModifiedTimeMixin):

    __parent__ = None

    content_type = alias('contentType')

    def __init__(self, data='', contentType='', filename=None, name=None):
        super(NamedFileMixin, self).__init__(data, contentType, filename)
        if name:
            self.name = name

    @property
    def length(self):
        return self.getSize()

    @readproperty
    def name(self):
        return safe_filename(nameFinder(self.filename))

    # XXX: Sadly we had defined the property __name__ as a 
    # readproperty on this object instead of alias for name.
    # so whenever __name__ is set it creates an additional entry on 
    # this object __dict__, which we do not want. So now we override
    # the __getattribute__ and __setattr__  methods to implement the alias
    # functionality between the __name__ and name properties, while 
    # respecting  previously set values on both
    def __getattribute__(self, name):
        if name == '__name__':
            if name in self.__dict__:
                return self.__dict__[name]
            return super(NamedFileMixin, self).__getattribute__('name')
        return super(NamedFileMixin, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if name == '__name__':
            if name in self.__dict__:
                self.__dict__[name] = value
            return super(NamedFileMixin, self).__setattr__('name', value)
        elif name == 'name':
            if '__name__' in self.__dict__:
                self.__dict__['__name__'] = value
        return super(NamedFileMixin, self).__setattr__(name, value)

    def __str__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)
    __repr__ = __str__

    @classmethod
    def nameFinder(cls, filename):
        return nameFinder(filename)


deprecated('NamedFile', 'DO NOT USE; Prefer NamedBlobFile')
@interface.implementer(INamedFile)
class NamedFile(NamedFileMixin, PloneNamedFile):
    size = read_alias('_size')


deprecated('NamedImage', 'DO NOT USE; Prefer NamedBlobImage')
@interface.implementer(INamedImage)
class NamedImage(NamedFileMixin, PloneNamedImage):
    size = read_alias('_size')


@interface.implementer(INamedBlobFile)
class NamedBlobFile(NamedFileMixin, PloneNamedBlobFile):

    @property
    def size(self):
        return super(NamedBlobFile, self).size

    @size.setter
    def size(self, nv):
        pass


@interface.implementer(INamedBlobImage)
class NamedBlobImage(NamedFileMixin, PloneNamedBlobImage):

    @property
    def size(self):
        return super(NamedBlobImage, self).size

    @size.setter
    def size(self, nv):
        pass


import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
    "Moved to nti.namedfile.constraints",
    "nti.namedfile.constraints",
    "FileConstraints"
)
