#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import mimetypes
from io import BytesIO
from six import get_function_globals

from zope import component

from zope.cachedescriptors.property import readproperty

from zope.file.file import File as ZFile

from zope.file.interfaces import IFile as IZFile

from zope.file.upload import nameFinder

from zope.interface import interfaces

from zope.mimetype.interfaces import IMimeTypeGetter

from plone.namedfile.file import NamedFile
from plone.namedfile.file import NamedBlobFile

from plone.namedfile.interfaces import IFile as INFile

from plone.namedfile.utils import get_contenttype

from nti.base.interfaces import INamedFile
from nti.base.interfaces import DEFAULT_CONTENT_TYPE as OCTET_STREAM

from nti.property.property import alias

logger = __import__('logging').getLogger(__name__)


# plone's guessing of content types is very limited compared to what zope does;
# let's use that instead. But many places have already imported it
# statically by name, so swizzle out the code
def _patched_get_contenttype(source=None, filename=None, default=OCTET_STREAM):
    file_type = getattr(source, 'contentType', None)
    if file_type:
        return file_type
    filename = getattr(source, 'filename', filename)
    mimeTypeGetter = component.queryUtility(IMimeTypeGetter)
    if mimeTypeGetter is not None:
        mimeType = mimeTypeGetter(data=getattr(source, 'data', None),
                                  content_type=None,
                                  name=nameFinder(filename))
    else:
        name = nameFinder(source) if not filename else filename
        mimeType = mimetypes.guess_type(name)[0] if name else None
    return mimeType or default


def _patch():
    # First, make plone's IFile extend zope's IFile. zope's IFile
    # declares the streaming interfaces open and openDetached while
    # plone's only declares the buffered 'data' interface, though
    # the blob-versions implement open and openDetached
    if INFile.__iro__ != (INFile, interfaces.Interface,):  # pragma: no cover
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
    # Rethink that, it's probably not right. __name__ is the
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

    def _name(self):
        return nameFinder(self)
    NamedFile.name = readproperty(_name)
    NamedBlobFile.name = readproperty(_name)

    # plone's non-blob-based files don't have open/openDetached,
    # so we fake it
    def _open(self, *unused_args, **unused_kwargs):
        return BytesIO(self.data)
    NamedFile.open = _open
    NamedFile.openDetached = _open

    # make zope file have a contentType
    ZFile.contentType = alias('mimeType')
    # also have a filename
    ZFile.filename = alias('__name__')
    # also have a display name
    ZFile.name = readproperty(_name)
    # set the data

    def _get_data(self):
        with self.open() as fp:
            return fp.read()

    def _set_data(self, data=b''):
        with self.open('w') as fp:
            return fp.write(data)
    ZFile.data = property(_get_data, _set_data)
    # return its size

    def _get_size(self):
        return self.size
    ZFile.getSize = _get_size
    # and make it and base file
    IZFile.__bases__ += (INamedFile,)

    # patch plone get_contenttype
    func_globals = get_function_globals(get_contenttype)
    func_globals['component'] = component
    func_globals['nameFinder'] = nameFinder
    func_globals['IMimeTypeGetter'] = IMimeTypeGetter
    get_contenttype.__code__ = _patched_get_contenttype.__code__


def patch():
    pass


_patch()
del _patch
