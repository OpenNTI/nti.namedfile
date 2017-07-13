#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from plone.namedfile.file import NamedFile
from plone.namedfile.file import NamedImage
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import get_contenttype

from plone.namedfile.interfaces import IFile as IPloneFile

from zope.file.file import File

from nti.base.interfaces import INamedFile

from nti.namedfile.monkey import patch
patch()
        
from nti.namedfile.tests import SharedConfiguringTestLayer


class TestMonkey(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_plone_file_patch(self):
        nf = NamedFile(data=b'data',
                       contentType='text/plain',
                       filename=u'foo.txt')

        nbf = NamedBlobFile(data=b'data',
                            contentType='text/plain',
                            filename=u'foo.txt')

        nif = NamedImage(data=b'data',
                         contentType='image/gif',
                         filename=u'foo.txt')
        for f in nf, nbf, nif:
            assert_that(f, validly_provides(INamedFile))
            assert_that(f, validly_provides(IPloneFile))
            assert_that(f, has_property('__name__', 'foo.txt'))

        # Check that we sniff the data using zope.mimetype.
        nf = NamedFile(data=b"<?xml?><config />")
        nf.mimeType = get_contenttype(file=nf)
        assert_that(nf, has_property('contentType', 'text/xml'))
        
    def test_zope_file_patch(self):
        zf = File(mimeType='text/plain')
        zf.filename = 'data.txt'

        assert_that(zf, validly_provides(INamedFile))
        assert_that(zf, verifiably_provides(INamedFile))
        
        assert_that(zf, has_property('name', is_('data.txt')))
        assert_that(zf, has_property('filename', is_('data.txt')))
        assert_that(zf, has_property('contentType', is_('text/plain')))

        zf.data = b'data'
        assert_that(zf.getSize(), is_(4))
        assert_that(zf.data, is_(b'data'))
        
        zf.name = 'data'
        assert_that(zf, has_property('name', is_('data')))
        assert_that(zf, has_property('filename', is_('data.txt')))
