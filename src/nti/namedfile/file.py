#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from zope import interface

from zope.mimetype.interfaces import mimeTypeConstraint

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedImage as PloneNamedImage
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile
from plone.namedfile.file import NamedBlobImage as PloneNamedBlobImage

from nti.coremetadata.mixins import CreatedAndModifiedTimeMixin

from .interfaces import INamedFile
from .interfaces import INamedImage
from .interfaces import INamedBlobFile
from .interfaces import INamedBlobImage

class NamedFileMixin(CreatedAndModifiedTimeMixin):

	name = None

	max_file_size = None
	allowed_extensions = ('*',)
	allowed_mime_types = ("*/*",)

	def is_file_size_allowed(self, size=None):
		size = self.getSize() if not size else size
		return not self.max_file_size or size <= self.max_file_size

	def is_mime_type_allowed(self, mime_type=None):
		mime_type = mime_type or self.contentType
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
		filename = filename or self.filename
		ext = os.path.splitext(filename.lower())[1] if filename else None
		result = (filename and (ext in self.allowed_extensions or \
								'*' in self.allowed_extensions))
		return result

	def __str__(self):
		return "%s(%s)" % (self.__class__.__name__, self.filename)
	__repr__ = __str__

@interface.implementer(INamedFile)
class NamedFile(NamedFileMixin, PloneNamedFile):
	mimeType = mime_type = u'application/vnd.nextthought.namedfile'

@interface.implementer(INamedImage)
class NamedImage(NamedFileMixin, PloneNamedImage):
	mimeType = mime_type = u'application/vnd.nextthought.namedimage'

@interface.implementer(INamedBlobFile)
class NamedBlobFile(NamedFileMixin, PloneNamedBlobFile):
	mimeType = mime_type = u'application/vnd.nextthought.namedblobfile'

@interface.implementer(INamedBlobImage)
class NamedBlobImage(NamedFileMixin, PloneNamedBlobImage):
	mimeType = mime_type = u'application/vnd.nextthought.namedblobimage'
