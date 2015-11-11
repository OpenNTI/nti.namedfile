#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import re

from zope import component
from zope import interface

from zope.location.interfaces import IContained

from zope.mimetype.interfaces import mimeTypeConstraint

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedImage as PloneNamedImage
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile
from plone.namedfile.file import NamedBlobImage as PloneNamedBlobImage

from nti.common.property import alias

from nti.coremetadata.mixins import CreatedAndModifiedTimeMixin

from .interfaces import INamedFile
from .interfaces import INamedImage
from .interfaces import INamedBlobFile
from .interfaces import INamedBlobImage
from .interfaces import IFileConstraints

@component.adapter(INamedFile)
@interface.implementer(IFileConstraints)
class FileConstraints(object):

	_v_file = None

	max_file_size = None
	allowed_extensions = ('*',)
	allowed_mime_types = ("*/*",)

	def __init__(self, context=None):  # make it adpater
		self._v_file = context

	def is_file_size_allowed(self, size=None):
		size = self._v_file.getSize() if self._v_file is not None and size is None else size
		result = not self.max_file_size or (size is not None and size <= self.max_file_size)
		return result

	def is_mime_type_allowed(self, mime_type=None):
		mime_type = mime_type or getattr(self._v_file, 'contentType', None)
		mime_type = mime_type.lower() if mime_type else mime_type
		if (not mime_type  # No input
			or not mimeTypeConstraint(mime_type)  # Invalid
			or not self.allowed_mime_types):  # Empty list: all excluded
			return False

		major, minor = mime_type.split('/')
		if major == '*' or minor == '*':
			return False  # Must be concrete

		for mt in self.allowed_mime_types:
			if mt == '*/*':
				return True  # Total wildcard

			mt = mt.lower()
			if mt == mime_type:
				return True

			amajor, aminor = mt.split('/')

			# Wildcards are only reasonable in the minor part,  e.g., text/*.
			if aminor == minor or aminor == '*':
				if major == amajor:
					return True
		return False

	def is_filename_allowed(self, filename=None):
		filename = filename or getattr(self._v_file, 'filename', None)
		ext = os.path.splitext(filename.lower())[1] if filename else None
		result = (filename and (ext in self.allowed_extensions or \
								'*' in self.allowed_extensions))
		return result

_nameFinder = re.compile(r'(.*[\\/:])?(.+)')

@interface.implementer(IContained)
class NamedFileMixin(CreatedAndModifiedTimeMixin):

	name = None
	
	__parent__ = None
	__name__ = alias('name')
	content_type = alias('contentType')
	
	def __init__(self, data='', contentType='', filename=None, name=None):
		super(NamedFileMixin, self).__init__(data=data,
											 contentType=contentType, 
											 filename=filename)
		self.name = name
		if not name:
			match = _nameFinder.match(name)
			self.name = match.group(2) if match else None
		
	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)
	__repr__ = __str__

@interface.implementer(INamedFile)
class NamedFile(NamedFileMixin, PloneNamedFile):
	pass

@interface.implementer(INamedImage)
class NamedImage(NamedFileMixin, PloneNamedImage):
	pass

@interface.implementer(INamedBlobFile)
class NamedBlobFile(NamedFileMixin, PloneNamedBlobFile):
	pass

@interface.implementer(INamedBlobImage)
class NamedBlobImage(NamedFileMixin, PloneNamedBlobImage):
	pass
