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

from nti.base._compat import text_

from nti.base.interfaces import DEFAULT_CONTENT_TYPE

from nti.base.interfaces import INamedFile

from nti.externalization.interfaces import StandardExternalFields 
from nti.externalization.interfaces import IInternalObjectExternalizer

from nti.externalization.datastructures import InterfaceObjectIO

from nti.mimetype.externalization import decorateMimeType

from nti.property.dataurl import encode

OID = StandardExternalFields.OID
NTIID = StandardExternalFields.NTIID


@component.adapter(INamedFile)
@interface.implementer(IInternalObjectExternalizer)
class _FileExporter(InterfaceObjectIO):

    _excluded_out_ivars_ = {'data', 'size', 'contentType'}
    _excluded_out_ivars_ = _excluded_out_ivars_.union(InterfaceObjectIO._excluded_out_ivars_)

    _ext_iface_upper_bound = INamedFile

    def toExternalObject(self, **kwargs):
        context = self._ext_replacement()
        contentType = getattr(context, 'contentType', None) or DEFAULT_CONTENT_TYPE
        [kwargs.pop(x, None) for x in ('name', 'decorate')]
        adapter = IInternalObjectExternalizer(context, None)
        if adapter is not None:
            result = adapter.toExternalObject(decorate=False, **kwargs)
        else:
            result = super(_FileExporter, self).toExternalObject(decorate=False, **kwargs)
            result['contentType'] = text_(contentType)
            decorateMimeType(context, result)
        result['url'] = encode(context.data, contentType)
        [result.pop(x, None) for x in (OID, NTIID)]
        return result
