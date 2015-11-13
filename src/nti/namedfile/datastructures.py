#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from zope.file.upload import nameFinder

from nti.common.dataurl import DataURL

from nti.coremetadata.schema import DataURI

from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.datastructures import AbstractDynamicObjectIO

from .file import safe_filename

from .file import NamedFile
from .file import NamedImage
from .file import NamedBlobFile
from .file import NamedBlobImage

from .interfaces import INamedFile
from .interfaces import INamedImage
from .interfaces import INamedBlobFile
from .interfaces import INamedBlobImage
from .interfaces import IInternalFileRef

OID = StandardExternalFields.OID
NTIID = StandardExternalFields.NTIID
MIMETYPE = StandardExternalFields.MIMETYPE

@component.adapter(INamedFile)
class NamedFileObjectIO(AbstractDynamicObjectIO):

	_excluded_out_ivars_ = {'data', 'size', 'contentType'}
	_excluded_out_ivars_ = _excluded_out_ivars_.union(AbstractDynamicObjectIO._excluded_out_ivars_)

	def __init__(self, ext_self):
		super(NamedFileObjectIO, self).__init__()
		self._ext_self = ext_self

	def _ext_replacement(self):
		return self._ext_self

	def _ext_all_possible_keys(self):
		return ()

	def _ext_mimeType(self, obj):
		return u'application/vnd.nextthought.namedfile'

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

		if 'filename' in parsed:
			ext_self.filename = safe_filename(parsed['filename'])
			# some times we get full paths
			name_found = nameFinder(ext_self)
			if name_found:
				ext_self.filename = safe_filename(name_found)
			name = ext_self.filename if not name else name
			updated = True

		# file id
		if name is not None:
			ext_self.name = name

		# contentType
		for name in ('FileMimeType', 'contentType', 'content_type', 'type'):
			if name in parsed:
				ext_self.contentType = bytes(parsed[name])
				updated = True
				break
		return updated

	def toExternalObject(self, mergeFrom=None, **kwargs):
		ext_dict = super(NamedFileObjectIO, self).toExternalObject(**kwargs)
		the_file = self._ext_replacement()
		contentType = the_file.contentType
		ext_dict['name'] = the_file.name or None
		ext_dict['filename'] = the_file.filename or None
		ext_dict[MIMETYPE] = self._ext_mimeType(the_file)
		ext_dict['contentType'] = ext_dict['FileMimeType'] = str(contentType or u'')
		return ext_dict

@component.adapter(INamedImage)
class NamedImageObjectIO(NamedFileObjectIO):

	def _ext_mimeType(self, obj):
		return u'application/vnd.nextthought.namedimage'

@component.adapter(INamedBlobFile)
class NamedBlobFileObjectIO(NamedFileObjectIO):

	def _ext_mimeType(self, obj):
		return u'application/vnd.nextthought.namedblobfile'

@component.adapter(INamedBlobImage)
class NamedBlobImageObjectIO(NamedFileObjectIO):

	def _ext_mimeType(self, obj):
		return u'application/vnd.nextthought.namedblobimage'

def BaseFactory(ext_obj, file_factory, image_factory=None):
	factory = file_factory
	image_factory = image_factory or file_factory
	url = ext_obj.get('url') or ext_obj.get('value')
	contentType = 	ext_obj.get('FileMimeType') or \
					ext_obj.get('contentType') or \
					ext_obj.get('content_type')
	if url and url.startswith(b'data:'):
		ext_obj['url'] = DataURL(url)
		ext_obj.pop('value', None)
		if ext_obj['url'].mimeType.startswith('image/'):
			factory = image_factory
	elif contentType and contentType.lower().startswith('image/'):
		factory = image_factory
	return factory

def NamedFileFactory(ext_obj):
	result = BaseFactory(ext_obj, NamedFile, NamedFile)
	return  result

def NamedImageFactory(ext_obj):
	result = BaseFactory(ext_obj, NamedImage, NamedImage)
	return  result

def NamedBlobFileFactory(ext_obj):
	result = BaseFactory(ext_obj, NamedBlobFile, NamedBlobImage)
	return  result

def NamedBlobImageFactory(ext_obj):
	result = BaseFactory(ext_obj, NamedBlobImage, NamedBlobImage)
	return  result
