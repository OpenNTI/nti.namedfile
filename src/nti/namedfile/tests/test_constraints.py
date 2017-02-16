#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import all_of
from hamcrest import is_not
from hamcrest import has_entry
from hamcrest import assert_that
does_not = is_not

import unittest

from nti.namedfile.file import NamedFile
from nti.namedfile.constraints import FileConstraints

from nti.namedfile.tests import SharedConfiguringTestLayer

from nti.externalization.tests import externalizes


class TestNamedFile(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_restrictions(self):
        named = NamedFile(data=b'data',
                          contentType='image/gif',
                          filename='zpt.gif')
        internal = FileConstraints(named)
        internal.max_file_size = 1
        internal.allowed_extensions = ('.doc',)
        internal.allowed_mime_types = ('image/jpeg',)
        assert_that(internal.is_file_size_allowed(), is_(False))
        assert_that(internal.is_mime_type_allowed(), is_(False))
        assert_that(internal.is_filename_allowed(), is_(False))

        assert_that(internal, 
                    externalizes(
                        all_of(has_entry('Class', 'FileConstraints'),
                               has_entry('max_file_size', 1),
                               has_entry('allowed_extensions', is_([u'.doc'])),
                               has_entry('allowed_mime_types', is_(['image/jpeg'])))))

        named = NamedFile(data=b'data',
                          contentType='image/gif',
                          filename='zpt.gif')
        internal = FileConstraints(named)
        internal.allowed_extensions = ('.GIF',)
        internal.allowed_mime_types = ('image/gif',)
        assert_that(internal.is_file_size_allowed(), is_(True))
        assert_that(internal.is_mime_type_allowed(), is_(True))
        assert_that(internal.is_filename_allowed(), is_(True))
