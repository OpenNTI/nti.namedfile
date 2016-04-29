#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

from zope import interface

from zope.cachedescriptors.property import readproperty

from plone.namedfile.interfaces import INamed as IPloneNamed

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedImage as PloneNamedImage
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile
from plone.namedfile.file import NamedBlobImage as PloneNamedBlobImage

from nti.common.property import alias

from nti.coremetadata.mixins import CreatedAndModifiedTimeMixin

from nti.namedfile.interfaces import IFile
from nti.namedfile.interfaces import INamedFile
from nti.namedfile.interfaces import INamedImage
from nti.namedfile.interfaces import INamedBlobFile
from nti.namedfile.interfaces import INamedBlobImage

_nameFinder = re.compile(r'(.*[\\/:])?(.+)')

def safe_filename(s):
	return re.sub(r'[/<>:"\\|?*]+', '', s) if s else s

def nameFinder(filename):
	match = _nameFinder.match(filename) if filename else None
	result = match.group(2) if match else None
	return result
name_finder = nameFinder

class NamedFileMixin(CreatedAndModifiedTimeMixin):

	name = None

	__parent__ = None

	content_type = alias('contentType')

	def __init__(self, data='', contentType='', filename=None, name=None):
		super(NamedFileMixin, self).__init__(data=data,
											 contentType=contentType,
											 filename=filename)
		self.name = name or self.nameFinder(filename)

	@property
	def length(self):
		return self.getSize()

	@readproperty
	def __name__(self):
		return self.name

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)
	__repr__ = __str__

	@classmethod
	def nameFinder(cls, filename):
		return nameFinder(filename)

@interface.implementer(INamedFile)
class NamedFile(NamedFileMixin, PloneNamedFile):
	pass

@interface.implementer(INamedImage)
class NamedImage(NamedFileMixin, PloneNamedImage):
	pass

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

def get_file_name(context):
	result = None
	if IFile.providedBy(context):
		result = context.name
	if not result and IPloneNamed.providedBy(context):
		result = NamedFileMixin.nameFinder(context.filename) or context.filename
	return result

import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecatedFrom(
	"Moved to nti.namedfile.constraints",
	"nti.namedfile.constraints",
	"FileConstraints"
)