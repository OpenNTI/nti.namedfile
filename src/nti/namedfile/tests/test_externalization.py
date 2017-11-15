#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import has_entries

import unittest

from zope import interface

from nti.base.interfaces import INamedFile

from nti.externalization.externalization import to_external_object

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.namedfile.externalization import _FileExporter

from nti.namedfile.tests import SharedConfiguringTestLayer

GIF_DATAURL = 'data:image/gif;base64,R0lGODlhCwALAIAAAAAA3pn/ZiH5BAEAAAEALAAAAAALAAsAAAIUhA+hkcuO4lmNVindo7qyrIXiGBYAOw=='


class TestExternalization(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_exporter(self):
        ext_obj = {
            'MimeType': 'application/vnd.nextthought.namedblobfile',
            'value': GIF_DATAURL,
            'filename': u'ichigo.gif',
            'name': u'ichigo.gif'
        }

        factory = find_factory_for(ext_obj)
        internal = factory()
        update_from_external_object(internal, ext_obj, require_updater=True)

        ext_obj = to_external_object(internal, name='exporter')
        assert_that(ext_obj,
                    has_entries('contentType', 'image/gif',
                                'name', 'ichigo.gif',
                                'url', GIF_DATAURL,
                                'MimeType', 'application/vnd.nextthought.namedblobimage'))

    def test_coverage(self):
        @interface.implementer(INamedFile)
        class Bleach(object):
            data = b'ichigo'
            filename = 'ichigo.txt'

        exporter = _FileExporter(Bleach(), INamedFile)
        assert_that(exporter.toExternalObject(),
                    has_entries('filename', 'ichigo.txt',
                                'url', 'data:application/octet-stream;base64,aWNoaWdv'))
