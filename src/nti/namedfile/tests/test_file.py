#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import all_of
from hamcrest import is_not
from hamcrest import has_key
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

import unittest

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.namedfile.file import NamedFile
from nti.namedfile.file import FileConstraints

from nti.namedfile.tests import SharedConfiguringTestLayer

from nti.externalization.tests import externalizes

GIF_DATAURL = b'data:image/gif;base64,R0lGODlhCwALAIAAAAAA3pn/ZiH5BAEAAAEALAAAAAALAAsAAAIUhA+hkcuO4lmNVindo7qyrIXiGBYAOw=='

class TestNamedFile(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_restrictions(self):
		named = NamedFile(data=GIF_DATAURL, contentType='image/gif', filename='zpt.gif')
		rn = FileConstraints(named)
		rn.max_file_size = 1
		rn.allowed_extensions = ('*.doc',)
		rn.allowed_mime_types = ('image/jpeg',)
		assert_that(rn.is_file_size_allowed(), is_(False))
		assert_that(rn.is_mime_type_allowed(), is_(False))
		assert_that(rn.is_filename_allowed(), is_(False))

	def test_namedfile(self):
		ext_obj = {
			'MimeType': 'application/vnd.nextthought.namedfile',
			'value': GIF_DATAURL,
			'filename': r'file.gif',
			'name':'ichigo'
		}

		factory = find_factory_for(ext_obj)
		assert_that(factory, is_not(none()))

		internal = factory()
		update_from_external_object(internal, ext_obj, require_updater=True)

		# value changed to URI
		assert_that(ext_obj, has_key('url'))
		assert_that(ext_obj, does_not(has_key('value')))

		assert_that(internal, has_property('contentType', 'image/gif'))
		assert_that(internal, has_property('filename', 'file.gif'))
		assert_that(internal, has_property('name', 'ichigo'))

		assert_that(internal, externalizes(all_of(has_key('FileMimeType'),
												  has_key('filename'),
												  has_key('name'))))
		
	def test_namefinder(self):
		s = NamedFile.nameFinder("ichigo")
		assert_that(s, is_('ichigo'))

		s = NamedFile.nameFinder("/users/aizen/bankai.gif")
		assert_that(s, is_('bankai.gif'))
		
		s = NamedFile.nameFinder("c:\\users\\rukia\\shikai.zip")
		assert_that(s, is_('shikai.zip'))


