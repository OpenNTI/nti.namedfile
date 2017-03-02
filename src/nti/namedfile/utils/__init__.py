#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://github.com/plone/plone.namedfile/blob/master/plone/namedfile/utils/__init__.py

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import struct

try:
    from cStringIO import StringIO
except ImportError:
    from six import StringIO

from PIL import Image

from nti.namedfile.utils.jpeg_utils import process_jpeg

from nti.namedfile.utils.png_utils import process_png

from nti.namedfile.utils.tiff_utils import process_tiff


def _ensure_data(image):
    data = None
    if getattr(image, 'read', None):
        data = image.read()
        image.seek(0)
    else:
        data = image
    return str(data)


def getImageInfo(data):
    data = _ensure_data(data)
    size = len(data)
    content_type = None
    width, height = -1, -1
    # handle GIFs
    if size >= 10 and data[:6] in (b'GIF87a', b'GIF89a'):
        content_type = 'image/gif'
        w, h = struct.unpack(b'<HH', data[6:10])
        width = int(w)
        height = int(h)
    # handle PNG
    elif data[:8] == b'\211PNG\r\n\032\n':    
        content_type, width, height = process_png(data)
    # handle JPEGs
    elif data[:2] == b'\377\330':    
        content_type, width, height = process_jpeg(data)
    # handle BMPs
    elif size >= 30 and data.startswith(b'BM'):
        kind = struct.unpack(b'<H', data[14:16])[0]
        if kind == 40:  # Windows 3.x bitmap
            content_type = 'image/x-ms-bmp'
            width, height = struct.unpack(b'<LL', data[18:26])
    elif size >= 8 and data[:4] in (b"II\052\000", b"MM\000\052"):
        content_type, width, height = process_tiff(data)
    # Use PIL / Pillow to determ Image Information
    elif data:
        try:
            img = Image.open(StringIO(data))
            width, height = img.size
            content_type = img.format or  u''
            if content_type.lower() == 'tiff':
                content_type = 'image/tiff'
        except Exception as e:
            logger.exception(e)
    # return
    logger.debug('Image Info (Type: %s, Width: %s, Height: %s)',
                 content_type, width, height)
    return content_type, width, height
