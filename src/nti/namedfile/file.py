#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import re

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.deprecation import deprecated

from zope.file.upload import nameFinder

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

logger = __import__('logging').getLogger(__name__)


def get_context_name(context):
    result = None
    if hasattr(context, 'name'):
        result = context.name
    if not result and INamed.providedBy(context):
        result = nameFinder(context)
    return result
get_file_name = get_context_name


def safe_filename(s):
    __traceback_info__ = s
    if s:
        try:
            s = s.encode("ascii", 'xmlcharrefreplace')
        except Exception: # pragma: no cover
            pass
        s = re.sub(r'[/<>:;"\\|#?*\s]+', '_', s)
        s = re.sub(r'&', '_', s)
        try:
            s = text_(s)
        except UnicodeDecodeError: # pragma: no cover
            s = s.decode('utf-8')
    return s


class NamedFileMixin(CreatedAndModifiedTimeMixin):

    __parent__ = None

    content_type = alias('contentType')

    def __init__(self, data='', contentType='', filename=None, name=None):
        super(NamedFileMixin, self).__init__(data, contentType, filename or name)
        if name:
            self.name = name

    @property
    def length(self):
        return self.getSize()

    @readproperty
    def name(self):
        return nameFinder(self)

    # XXX: Sadly we have defined the property __name__ as a
    # readproperty on the name property instead of filename
    # so whenever __name__ is set it creates an additional entry on
    # this object __dict__, which we did not want.
    @readproperty
    def __name__(self):
        return self.name

    def __str__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)
    __repr__ = __str__


deprecated('NamedFile', 'DO NOT USE; Prefer NamedBlobFile')
@interface.implementer(INamedFile)
class NamedFile(NamedFileMixin, PloneNamedFile):
    size = read_alias('_size')
    __external_mimeType__ = 'application/vnd.nextthought.namedfile'


deprecated('NamedImage', 'DO NOT USE; Prefer NamedBlobImage')
@interface.implementer(INamedImage)
class NamedImage(NamedFileMixin, PloneNamedImage):
    size = read_alias('_size')
    __external_mimeType__ = 'application/vnd.nextthought.namedimage'


@interface.implementer(INamedBlobFile)
class NamedBlobFile(NamedFileMixin, PloneNamedBlobFile):

    __external_mimeType__ = 'application/vnd.nextthought.namedblobfile'

    @property
    def size(self):
        return super(NamedBlobFile, self).size

    @size.setter
    def size(self, nv):
        pass


@interface.implementer(INamedBlobImage)
class NamedBlobImage(NamedFileMixin, PloneNamedBlobImage):

    __external_mimeType__ = 'application/vnd.nextthought.namedblobimage'

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
