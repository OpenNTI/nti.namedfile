#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from zope.file.file import File as ZopeFile

from zope.file.interfaces import IFile as IZopeFile

from zope.file.upload import nameFinder

from nti.base._compat import text_
from nti.base._compat import bytes_

from nti.base.interfaces import DEFAULT_CONTENT_TYPE

from nti.property.schema import DataURI

from nti.externalization.datastructures import AbstractDynamicObjectIO

from nti.externalization.interfaces import StandardExternalFields

from nti.namedfile.file import NamedBlobFile
from nti.namedfile.file import NamedBlobImage

from nti.namedfile.interfaces import INamedFile
from nti.namedfile.interfaces import INamedImage
from nti.namedfile.interfaces import INamedBlobFile
from nti.namedfile.interfaces import INamedBlobImage
from nti.namedfile.interfaces import IInternalFileRef

from nti.property.dataurl import DataURL

OID = StandardExternalFields.OID
NTIID = StandardExternalFields.NTIID
MIMETYPE = StandardExternalFields.MIMETYPE

logger = __import__('logging').getLogger(__name__)


@component.adapter(INamedFile)
class NamedFileObjectIO(AbstractDynamicObjectIO):

    _excluded_out_ivars_ = {'data', 'size', 'contentType'}
    _excluded_out_ivars_ = _excluded_out_ivars_.union(
        AbstractDynamicObjectIO._excluded_out_ivars_)

    def __init__(self, ext_self):
        super(NamedFileObjectIO, self).__init__()
        self._ext_self = ext_self

    def _ext_replacement(self):
        return self._ext_self

    def _ext_all_possible_keys(self):
        return ()

    def _ext_mimeType(self, unused_obj):
        return 'application/vnd.nextthought.namedfile'

    def is_internal_fileref(self, parsed):
        return parsed.get(OID) or parsed.get(NTIID)

    # For symmetry with the other response types,
    # we accept either 'url' or 'value'

    def _ext_remove_excluded(self, parsed):
        # then remove excluded in fields to avoid any hint of a copy
        for name in self._excluded_in_ivars_:
            parsed.pop(name, None)

        # remove invalid url/value data spec
        for name in ('url', 'value'):
            value = parsed.get(name)
            if not DataURI.is_valid_data_uri(value):
                parsed.pop(name, None)

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        ext_self = self._ext_replacement()
        if self.is_internal_fileref(parsed):
            # when updating from an external source and either an
            # NTIID/OID is provided save the reference
            interface.alsoProvides(ext_self, IInternalFileRef)
            ext_self.reference = parsed.get(OID) or parsed.get(NTIID)
            # then remove excluded in fields to avoid any hint of a copy
            self._ext_remove_excluded(parsed)
        # start update
        updated = super(NamedFileObjectIO, self).updateFromExternalObject(parsed, *args, **kwargs)
        ext_self = self._ext_replacement()
        url = parsed.get('url') or parsed.get('value')
        name = parsed.get('name') or parsed.get('Name')
        if url:
            data_url = DataURI(__name__='url').fromUnicode(url)
            ext_self.contentType = data_url.mimeType
            ext_self.data = data_url.data
            updated = True
        if name and not parsed.get('filename', None):
            parsed['filename'] = name
        if 'filename' in parsed:
            ext_self.filename = parsed['filename']
            # some times we get full paths
            name_found = nameFinder(ext_self)
            if name_found:
                ext_self.filename = name_found
            name = ext_self.filename if not name else name
            updated = True
        # display name
        if name and name != ext_self.filename:
            ext_self.name = name
        # contentType
        # XXX: We are IContentTypeAware constrained to have ASCII `mimeType`
        for name in ('FileMimeType', 'contentType'):
            if name in parsed:
                ext_self.contentType = bytes_(parsed[name])
                updated = True
                break
        return updated

    def toExternalObject(self, *args, **kwargs):
        ext_dict = super(NamedFileObjectIO, self).toExternalObject(*args, **kwargs)
        the_file = self._ext_replacement()
        name = getattr(the_file, 'name', None)
        filename = getattr(the_file, 'filename', None)
        ext_dict['filename'] = filename
        ext_dict['name'] = name or filename
        ext_dict[MIMETYPE] = self._ext_mimeType(the_file)
        contentType = getattr(the_file, 'contentType', None)
        contentType = contentType or DEFAULT_CONTENT_TYPE
        ext_dict['contentType'] = ext_dict['FileMimeType'] = text_(contentType)
        return ext_dict


@component.adapter(INamedImage)
class NamedImageObjectIO(NamedFileObjectIO):

    def _ext_mimeType(self, unused_obj):
        return 'application/vnd.nextthought.namedimage'


@component.adapter(INamedBlobFile)
class NamedBlobFileObjectIO(NamedFileObjectIO):

    def _ext_mimeType(self, unused_obj):
        return 'application/vnd.nextthought.namedblobfile'


@component.adapter(INamedBlobImage)
class NamedBlobImageObjectIO(NamedFileObjectIO):

    def _ext_mimeType(self, unused_obj):
        return 'application/vnd.nextthought.namedblobimage'


@component.adapter(IZopeFile)
class ZopeFileObjectIO(NamedFileObjectIO):

    def _ext_mimeType(self, unused_obj):
        return 'application/vnd.nextthought.zopefile'


def getContentType(ext_obj):
    return ext_obj.get('FileMimeType') \
        or ext_obj.get('contentType')  \
        or ext_obj.get('content_type')


def BaseFactory(ext_obj, file_factory, image_factory=None):
    factory = file_factory
    image_factory = image_factory or file_factory
    url = ext_obj.get('url') or ext_obj.get('value')
    contentType = getContentType(ext_obj)
    if url and url.startswith('data:'):
        ext_obj['url'] = DataURL(url)
        ext_obj.pop('value', None)
        if ext_obj['url'].mimeType.startswith('image/'):
            factory = image_factory
    elif contentType and contentType.lower().startswith('image/'):
        factory = image_factory
    return factory


def NamedFileFactory(ext_obj):
    return BaseFactory(ext_obj, NamedBlobFile, NamedBlobFile)


def NamedImageFactory(ext_obj):
    return BaseFactory(ext_obj, NamedBlobImage, NamedBlobImage)


def NamedBlobFileFactory(ext_obj):
    return BaseFactory(ext_obj, NamedBlobFile, NamedBlobImage)


def NamedBlobImageFactory(ext_obj):
    return BaseFactory(ext_obj, NamedBlobImage, NamedBlobImage)


def ZopeFileFactory(ext_obj):
    return BaseFactory(ext_obj, ZopeFile, ZopeFile)
