#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that

import unittest

from zope.file.file import File as ZopeFile

from nti.namedfile.datastructures import ZopeFileObjectIO
from nti.namedfile.datastructures import NamedFileObjectIO
from nti.namedfile.datastructures import NamedImageObjectIO
from nti.namedfile.datastructures import NamedBlobFileObjectIO

from nti.namedfile.datastructures import ZopeFileFactory
from nti.namedfile.datastructures import NamedFileFactory
from nti.namedfile.datastructures import NamedImageFactory
from nti.namedfile.datastructures import NamedBlobFileFactory
from nti.namedfile.datastructures import NamedBlobImageFactory

from nti.namedfile.file import NamedBlobFile
from nti.namedfile.file import NamedBlobImage

from nti.namedfile.tests import SharedConfiguringTestLayer


class TestDatastructures(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_ext_mimeType(self):
        nio = NamedFileObjectIO(None)
        assert_that(nio._ext_mimeType(), is_(none()))

        nio = NamedImageObjectIO(None)
        assert_that(nio._ext_mimeType(),
                    is_('application/vnd.nextthought.namedimage'))

        nio = NamedImageObjectIO(None)
        assert_that(nio._ext_mimeType(),
                    is_('application/vnd.nextthought.namedimage'))

        nio = NamedBlobFileObjectIO(None)
        assert_that(nio._ext_mimeType(),
                    is_('application/vnd.nextthought.namedblobfile'))

        nio = ZopeFileObjectIO(None)
        assert_that(nio._ext_mimeType(),
                    is_('application/vnd.nextthought.zopefile'))

    def test_factory(self):
        assert_that(NamedFileFactory({'contentType': 'image/gif'})(),
                    is_(NamedBlobFile))

        assert_that(NamedImageFactory({'contentType': 'image/gif'})(),
                    is_(NamedBlobImage))

        assert_that(NamedBlobFileFactory({'contentType': 'image/gif'})(),
                    is_(NamedBlobImage))

        assert_that(NamedBlobImageFactory({'contentType': 'image/gif'})(),
                    is_(NamedBlobImage))

        assert_that(ZopeFileFactory({'contentType': 'image/gif'})(),
                    is_(ZopeFile))
