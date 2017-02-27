#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides

import unittest

from plone.namedfile import file as plone_file

from plone.namedfile.interfaces import IFile as IPloneFile

from nti.namedfile.monkey import patch

from nti.namedfile.tests import SharedConfiguringTestLayer


class TestMonkey(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_patch(self):
        patch()

        nf = plone_file.NamedFile(data=b'data',
                             contentType=b'text/plain',
                             filename='foo.txt')

        nbf = plone_file.NamedBlobFile(data=b'data',
                                  contentType=b'text/plain',
                                  filename='foo.txt')

        nif = plone_file.NamedBlobFile(data=b'data',
                                  contentType=b'image/gif',
                                  filename='foo.txt')
        for f in nf, nbf, nif:
            assert_that(f, validly_provides(IPloneFile))
            assert_that(f, has_property('__name__', 'foo.txt'))

        # Check that we sniff the data using zope.mimetype.
        nf = plone_file.NamedFile(data=b"<?xml?><config />")
        nf.mimeType = plone_file.get_contenttype(file=nf)
        assert_that(nf, has_property('contentType', 'text/xml'))
