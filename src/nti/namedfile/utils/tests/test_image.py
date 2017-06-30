#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

import os
import unittest

from plone.namedfile.file import NamedImage

from nti.namedfile.tests import SharedConfiguringTestLayer

zptlogo = (
    'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    '\x00A\x00;'
)


class TestImage(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def _make_image(self, *args, **kw):
        return NamedImage(*args, **kw)

    def get_file(self, filename):
        filename = os.path.join(os.path.dirname(__file__), filename)
        with open(filename, "rb") as fp:
            return fp.read()

    def test_zptlogo(self):
        image = self._make_image()
        image._setData(zptlogo)
        assert_that(image.contentType, is_('image/gif'))
        assert_that(image.getImageSize(), is_((16, 16)))

    def test_gif(self):
        image = self._make_image()
        image._setData(self.get_file("image.gif"))
        assert_that(image.contentType, is_('image/gif'))
        assert_that(image.getImageSize(), is_((200, 200)))

    def test_png(self):
        image = self._make_image()
        image._setData(self.get_file("image.png"))
        assert_that(image.contentType, is_('image/png'))
        assert_that(image.getImageSize(), is_((200, 200)))

    def test_jpeg(self):
        image = self._make_image()
        image._setData(self.get_file("image.jpg"))
        assert_that(image.contentType, is_('image/jpeg'))
        assert_that(image.getImageSize(), is_((500, 200)))
        
    def test_tiff(self):
        image = self._make_image()
        image._setData(self.get_file("image.tiff"))
        assert_that(image.contentType, is_('image/tiff'))
        assert_that(image.getImageSize(), is_((1728, 2376)))
    
    def test_bmp(self):
        image = self._make_image()
        image._setData(self.get_file("image.bmp"))
        assert_that(image.contentType, is_('image/x-ms-bmp'))
        assert_that(image.getImageSize(), is_((256, 256)))
