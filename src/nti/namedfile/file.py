#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import hashlib
import os

from slugify import Slugify

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.deprecation import deprecated

from zope.file.upload import nameFinder

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedImage as PloneNamedImage
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile
from plone.namedfile.file import NamedBlobImage as PloneNamedBlobImage

from nti.base._compat import bytes_

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


def trim_filename(filename, max_len):
    if len(filename) > max_len:
        trim_by = len(filename) - max_len
        name, ext = os.path.splitext(filename)
        if trim_by >= len(name):
            filename = filename[:-trim_by]
        else:
            filename = name[:-trim_by] + ext
    return filename


def hexdigest(data, salt=None):
    data = bytes_(data)
    salt = bytes_(salt or b'')
    hasher = hashlib.sha256()
    hasher.update(data + salt)
    return hasher.hexdigest()


slugify_filename = Slugify()
slugify_filename.separator = '_'
slugify_filename.safe_chars = '_-.'


def safe_filename(s, max_len=255, hash_len=10):
    candidate_name = slugify_filename(s)

    # May need to trim to max_len
    if len(candidate_name) > max_len:
        suffix_len = hash_len + 1

        # If we only have enough room for the hash, return that
        if suffix_len >= max_len:
            return hexdigest(s)[:max_len]

        trimmed_len = max_len - suffix_len
        trimmed_name = trim_filename(candidate_name, trimmed_len)

        # Hash using the original name, which is more likely unique
        suffix = hexdigest(s)[:hash_len]

        name, ext = os.path.splitext(trimmed_name)
        candidate_name = "%s-%s%s" % (name, suffix, ext)

    return candidate_name


class NamedFileMixin(CreatedAndModifiedTimeMixin):

    __parent__ = None

    content_type = alias('contentType')

    def __init__(self, data='', contentType='', filename=None, name=None):
        super(NamedFileMixin, self).__init__(
            data, contentType, filename or name)
        if name:
            self.name = name

    @property
    def length(self):
        return self.getSize()

    @readproperty
    def name(self):  # pylint: disable=method-hidden
        return nameFinder(self)

    # Sadly we have defined the property __name__ as a
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
