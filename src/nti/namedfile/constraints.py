#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from zope import component
from zope import interface

from zope.mimetype.interfaces import IContentTypeAware

from nti.mimetype.mimetype import mimeTypeConstraint

from nti.namedfile.interfaces import INamedFile
from nti.namedfile.interfaces import IFileConstraints

@component.adapter(INamedFile)
@interface.implementer(IFileConstraints, IContentTypeAware)
class FileConstraints(object):

	mimeType = mime_type = u'application/vnd.nextthought.namedfileconstraints'

	_v_file = None

	max_files = 2
	max_file_size = None
	allowed_extensions = ('*',)
	allowed_mime_types = ("*/*",)

	parameters = {} # IContentTypeAware

	def __init__(self, context=None):  # make it adpater
		self._v_file = context

	def is_file_size_allowed(self, size=None):
		size = self._v_file.getSize() if self._v_file is not None and size is None else size
		result = not self.max_file_size or (size is not None and size <= self.max_file_size)
		return result

	def is_mime_type_allowed(self, mime_type=None):
		mime_type = mime_type or getattr(self._v_file, 'contentType', None)
		mime_type = mime_type.lower() if mime_type else mime_type
		if (	not mime_type  # No input
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
			idx = aminor.find(';')
			if idx != -1: # ignore params
				aminor = aminor[0:idx]

			# Wildcards are only reasonable in the minor part,  e.g., text/*.
			if aminor == minor or aminor == '*':
				if major == amajor:
					return True
		return False

	def is_filename_allowed(self, filename=None):
		filename = filename or getattr(self._v_file, 'filename', None)
		ext = os.path.splitext(filename.lower())[1] if filename else None
		lowered_exts = (x.lower() for x in self.allowed_extensions or ())
		result = False
		if filename:
			result = 	not self.allowed_extensions \
					or  '*' in self.allowed_extensions \
					or	ext in lowered_exts
		return result
