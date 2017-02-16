#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import has_property

import unittest

import plone.namedfile.file as nfile
import plone.namedfile.interfaces as nfile_interfaces

from nti.namedfile.monkey import patch

from nti.namedfile.tests import SharedConfiguringTestLayer

from nti.testing.matchers import validly_provides


class TestMonkey(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_patch(self):
        patch()

        nf = nfile.NamedFile(data=b'data',
                             contentType=b'text/plain',
                             filename='foo.txt')
        nbf = nfile.NamedBlobFile(data=b'data',
                                  contentType=b'text/plain',
                                  filename='foo.txt')
        nif = nfile.NamedBlobFile(data=b'data',
                                  contentType=b'image/gif',
                                  filename='foo.txt')
        for f in nf, nbf, nif:
            assert_that(f, validly_provides(nfile_interfaces.IFile))
            assert_that(f, has_property('__name__', 'foo.txt'))

        # Check that we sniff the data using zope.mimetype.
        nf = nfile.NamedFile(data=b"<?xml?><config />")
        nf.mimeType = nfile.get_contenttype(file=nf)
        assert_that(nf, has_property('contentType', 'text/xml'))
