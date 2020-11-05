#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

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

from zope import interface

from plone.namedfile.file import NamedFile as PloneNamedFile
from plone.namedfile.file import NamedBlobFile as PloneNamedBlobFile

from nti.base.interfaces import INamedFile

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.externalization.tests import externalizes

from nti.namedfile.file import NamedFile
from nti.namedfile.file import NamedBlobFile
from nti.namedfile.file import NamedBlobImage

from nti.namedfile.file import safe_filename
from nti.namedfile.file import get_context_name

from nti.namedfile.tests import SharedConfiguringTestLayer


GIF_DATAURL = 'data:image/gif;base64,R0lGODlhCwALAIAAAAAA3pn/ZiH5BAEAAAEALAAAAAALAAsAAAIUhA+hkcuO4lmNVindo7qyrIXiGBYAOw=='


class TestNamedFile(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_namedfile(self):
        ext_obj = {
            'MimeType': 'application/vnd.nextthought.namedblobfile',
            'value': GIF_DATAURL,
            'name': u'file.gif',
            'OID': 'tag:nextthought.com,2011-10:aizen-OID-0x01:666f6f'
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
        assert_that(internal, has_property('name', 'file.gif'))

        assert_that(internal, externalizes(all_of(has_key('FileMimeType'),
                                                  has_key('filename'),
                                                  has_key('name'))))

    def test_namedblob(self):
        s = NamedBlobFile(b'image', 'image/gif', u'image.gif', u'image.gif')
        str(s)  # coverage
        assert_that(s, has_property('size', is_(5)))
        assert_that(s, has_property('length', is_(5)))
        assert_that(s, has_property('data', is_(b'image')))
        assert_that(s, has_property('filename', is_('image.gif')))
        assert_that(s, has_property('__name__', is_('image.gif')))
        assert_that(s, has_property('contentType', is_('image/gif')))
        s.size = 888
        assert_that(s, has_property('size', is_(5)))

    def test_namedblobimage(self):
        s = NamedBlobImage(b'image', 'image/gif', u'image.gif', u'image.gif')
        assert_that(s, has_property('size', is_(5)))
        s.size = 888
        assert_that(s, has_property('size', is_(5)))

    def test_interface(self):
        for factory in (NamedBlobFile,
                        NamedFile,
                        PloneNamedFile,
                        PloneNamedBlobFile):
            s = factory()
            assert_that(s, validly_provides(INamedFile))

    def test_get_context_name(self):
        @interface.implementer(INamedFile)
        class Bleach(object):
            name = None
            filename = 'ichigo.txt'
        assert_that(get_context_name(Bleach()),
                    is_('ichigo.txt'))

    def test_safe_filename_invalid_chars(self):
        assert_that(safe_filename('/ichigo&/<>:;"\\|#?* \t.txt'),
                    is_('ichigo_.txt'))

    def test_safe_filename_exceeds_max(self):
        assert_that(safe_filename("testing-abc123.tmp", max_len=15, hash_len=4),
                    is_(r"testin-65e1.tmp"))

        # If length of hash suffix (hash_len + 1) >= max length of base name (max_len - len(ext))
        assert_that(safe_filename("testing-abc123.tmp", max_len=15, hash_len=10),
                    is_(r"test-65e1555ce0"))

        # If length of hash suffix (hash_len + 1) >=  > max_len
        assert_that(safe_filename("testing-abc123.tmp", max_len=15, hash_len=20),
                    is_("65e1555ce0e3401"))

    def test_safe_filename_expansion_exceeds_max(self):
        filename = ("." * 254) + u"မိ"
        expected = ("." * 244) + u"-c4bd484eab"
        assert_that(safe_filename(filename),
                    is_(expected))
