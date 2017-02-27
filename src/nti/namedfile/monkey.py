#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import unicode_literals, print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from six import StringIO

from zope import component

from zope.file.interfaces import IFile as IZFile

from zope.file.upload import nameFinder

from zope.interface import interfaces

from zope.mimetype.interfaces import IMimeTypeGetter

from plone.namedfile import file as plone_file

from plone.namedfile.file import NamedFile
from plone.namedfile.file import NamedBlobFile

from plone.namedfile.interfaces import IFile as INFile

from plone.namedfile.utils import get_contenttype

from nti.namedfile.utils import getImageInfo

from nti.property.property import alias

OCTET_STREAM = 'application/octet-stream'


# plone's guessing of content types is very limited compared to what zope does;
# let's use that instead. But many places have already imported it
# statically by name, so swizzle out the code
def _patched_get_contenttype(file=None, filename=None, default=OCTET_STREAM):
    file_type = getattr(file, 'contentType', None)
    if file_type:
        return file_type
    filename = getattr(file, 'filename', filename)

    mimeTypeGetter = component.getUtility(IMimeTypeGetter)
    mimeType = mimeTypeGetter(data=getattr(file, 'data', None),
                              content_type=None,
                              name=nameFinder(filename))
    return mimeType or default


def _patch():
    # First, make plone's IFile extend zope's IFile. zope's IFile
    # declares the streaming interfaces open and openDetached while
    # plone's only declares the buffered 'data' interface, though
    # the blob-versions implement open and openDetached
    if INFile.__iro__ != (INFile, interfaces.Interface,):
        raise ImportError("Internals of plone.namedfile have changed")
    INFile.__bases__ = (IZFile,)

    # They are almost compatible, with a few minor differences we
    # fix up here.

    # size as a property (zope) vs getSize() (plone)
    NamedFile.size = property(NamedFile.getSize)
    # is already in the blob versions
    assert hasattr(NamedBlobFile, 'size')

    # zope.file.file is an ILocation. We say that __name__ is always the same
    # as filename...this is tricky because __name__ on a type means
    # the type name; only instances can see what's in the type's
    # __dict__ (and we can't assign to it). So we resort to sticking
    # in a base class.
    # TODO: Rethink that, it's probably not right. __name__ is the
    # name within the container; it may initially be based on
    # the filename, but they are probably different
    class _Base(object):
        __name__ = alias('filename')
    assert len(NamedFile.__bases__) == 1
    NamedFile.__bases__ += (_Base,)
    assert len(NamedBlobFile.__bases__) == 1
    NamedBlobFile.__bases__ += (_Base,)

    NamedFile.__parent__ = None
    NamedBlobFile.__parent__ = None

    # zope.file.file is IContentTypeAware, plonefile declares 'contentType'
    NamedFile.mimeType = alias('contentType')
    NamedBlobFile.mimeType = alias('contentType')
    # and it needs parameters (actually, zope.file.file doesn't get that
    # right either)
    # true this is unsafe but they are supposed to be read-only
    NamedFile.parameters = {}
    NamedBlobFile.parameters = {}

    # plone's non-blob-based files don't have open/openDetached,
    # so we fake it
    def _open(self, mode='r'):
        return StringIO(self.data)
    NamedFile.open = _open
    NamedFile.openDetached = _open

    func_globals = getattr(get_contenttype, 'func_globals')
    func_globals['component'] = component
    func_globals['nameFinder'] = nameFinder
    func_globals['IMimeTypeGetter'] = IMimeTypeGetter
    get_contenttype.__code__ = _patched_get_contenttype.__code__

    # use new code to get image info
    plone_file.getImageInfo = getImageInfo


def patch():
    pass

_patch()
del _patch
