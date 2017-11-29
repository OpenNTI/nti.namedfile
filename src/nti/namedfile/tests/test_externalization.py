#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_not
from hamcrest import has_key
from hamcrest import assert_that
from hamcrest import has_entries
does_not = is_not

import unittest

from zope import interface

from nti.base.interfaces import INamedFile

from nti.externalization.externalization import to_external_object

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.namedfile.externalization import _FileExporter

from nti.namedfile.tests import SharedConfiguringTestLayer


class TestExternalization(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_exporter(self):
        ext_obj = {
            'MimeType': 'application/vnd.nextthought.namedblobfile',
            'filename': u'ichigo.txt',
            'name': u'ichigo',
            'contentType': 'text/plain',
        }

        factory = find_factory_for(ext_obj)
        internal = factory()
        update_from_external_object(internal, ext_obj, require_updater=True)

        internal.data = b'ichigo'
        ext_obj = to_external_object(internal, name='exporter')
        assert_that(ext_obj,
                    has_entries('contentType', 'text/plain',
                                'name', 'ichigo',
                                'filename', 'ichigo.txt',
                                'url', 'data:text/plain;charset=US-ASCII;base64,aWNoaWdv',
                                'MimeType', 'application/vnd.nextthought.namedblobfile'))

    def test_coverage(self):
        @interface.implementer(INamedFile)
        class Bleach(object):
            data = b'ichigo'
            filename = 'ichigo.txt'

        exporter = _FileExporter(Bleach(), INamedFile)
        ext_obj = exporter.toExternalObject()
        assert_that(ext_obj,
                    has_entries('filename', 'ichigo.txt',
                                'url', 'data:application/octet-stream;base64,aWNoaWdv'))
        assert_that(ext_obj, 
                    does_not(has_key('NTIID')))

