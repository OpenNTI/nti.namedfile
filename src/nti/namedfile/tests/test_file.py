#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

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

from nti.testing.matchers import validly_provides

import unittest

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile

from nti.base.interfaces import INamedFile

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.externalization.tests import externalizes

from nti.namedfile.file import NamedFile
from nti.namedfile.file import NamedBlobFile

from nti.namedfile.tests import SharedConfiguringTestLayer


GIF_DATAURL = 'data:image/gif;base64,R0lGODlhCwALAIAAAAAA3pn/ZiH5BAEAAAEALAAAAAALAAsAAAIUhA+hkcuO4lmNVindo7qyrIXiGBYAOw=='


class TestNamedFile(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_namedfile(self):
        ext_obj = {
            'MimeType': 'application/vnd.nextthought.namedblobfile',
            'value': GIF_DATAURL,
            'filename': u'file.gif',
            'name': u'ichigo'
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

    def test_nameblob(self):
        s = NamedBlobFile(b'image', 'image/gif', u'image.gif')
        assert_that(s, has_property('size', is_(5)))
        assert_that(s, has_property('data', is_(b'image')))
        assert_that(s, has_property('filename', is_('image.gif')))
        assert_that(s, has_property('contentType', is_('image/gif')))
        s.size = 888
        assert_that(s, has_property('size', is_(5)))

    def test_interface(self):
        for factory in (NamedBlobFile,
                        NamedFile,
                        PloneNamedFile,
                        PloneNamedBlobFile):
            s = factory()
            assert_that(s, validly_provides(INamedFile))
