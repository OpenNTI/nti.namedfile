#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.base.interfaces import DEFAULT_CONTENT_TYPE

from nti.base.interfaces import INamedFile

from nti.externalization.interfaces import IInternalObjectExternalizer

from nti.externalization.externalization import to_external_object

from nti.property.dataurl import encode


@component.adapter(INamedFile)
@interface.implementer(IInternalObjectExternalizer)
class _FileExporter(object):

    def __init__(self, context):
        self.context = context

    def toExternalObject(self, **kwargs):
        kwargs.pop('decorate', None)
        context = self.context
        result = to_external_object(context, decorate=False, **kwargs)
        contentType = getattr(context, 'contentType',None) 
        contentType = contentType or DEFAULT_CONTENT_TYPE
        result['url'] = encode(context.data, contentType)
        return result
