#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from plone.namedfile.file import NamedFile
from plone.namedfile.file import NamedImage
from plone.namedfile.file import NamedBlobFile

from plone.namedfile.interfaces import IFile as IPloneFile

from plone.namedfile.utils import get_contenttype

from zope import component

from zope.file.file import File

from zope.mimetype.interfaces import IMimeTypeGetter

from nti.base.interfaces import INamedFile

from nti.namedfile.monkey import patch
patch()

from nti.namedfile.tests import SharedConfiguringTestLayer


class TestMonkey(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_plone_file_patch(self):
        nf = NamedFile(data=b'data',
                       contentType=b'text/plain',
                       filename=u'foo.txt')

        nbf = NamedBlobFile(data=b'data',
                            contentType=b'text/plain',
                            filename=u'foo.txt')

        nif = NamedImage(data=b'data',
                         contentType=b'image/gif',
                         filename=u'foo.txt')
        for f in nf, nbf, nif:
            assert_that(f, validly_provides(INamedFile))
            assert_that(f, verifiably_provides(IPloneFile))
            assert_that(f, has_property('__name__', 'foo.txt'))
            
        assert_that(nf.openDetached().read(),
                    is_(b'data'))

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

    def test_get_contenttype(self):
        class Ichigo(object):
            contentType = 'text/plain'
            filename = 'ichigo.txt'
        ichigo = Ichigo()
        assert_that(get_contenttype(ichigo), is_('text/plain'))

        ichigo.contentType = None
        assert_that(get_contenttype(ichigo), is_('text/plain'))

        class MimeTypeGetter(object):

            def __call__(self, *unused_args, **unused_kwargs):
                return 'text/plain'

        mimetype_getter = MimeTypeGetter()
        component.getGlobalSiteManager().registerUtility(mimetype_getter,
                                                         IMimeTypeGetter)

        assert_that(get_contenttype(ichigo), is_('text/plain'))

        component.getGlobalSiteManager().unregisterUtility(mimetype_getter,
                                                           IMimeTypeGetter)
