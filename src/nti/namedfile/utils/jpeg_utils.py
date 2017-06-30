#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://github.com/plone/plone.namedfile/blob/master/plone/namedfile/utils/jpeg_utils.py

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import struct

try:
    from cStringIO import StringIO
except ImportError:
    from six import StringIO


def process_jpeg(data):
    size = len(data)
    content_type, width, height = None, -1, -1
    # handle JPEGs
    if size >= 2 and data.startswith(b'\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            width = -1
            width = -1
            while b and ord(b) != 0xDA:
                while ord(b) != 0xFF:
                    b = jpeg.read(1)
                while ord(b) == 0xFF:
                    b = jpeg.read(1)
                if ord(b) >= 0xC0 and ord(b) <= 0xC3:
                    jpeg.read(3)
                    height, width = struct.unpack(b'>HH', jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(b'>H', jpeg.read(2))[0]) - 2)
                b = jpeg.read(1)
            width = int(width)
            height = int(height)
        except struct.error:
            pass
        except ValueError:
            pass
        except TypeError:
            pass
    # return
    return content_type, width, height
