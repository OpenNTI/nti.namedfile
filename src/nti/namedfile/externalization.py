#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

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

logger = __import__('logging').getLogger(__name__)


@component.adapter(INamedFile)
@interface.implementer(IInternalObjectExternalizer)
class _FileExporter(InterfaceObjectIO):

    _excluded_out_ivars_ = {'data', 'size', 'contentType'}
    _excluded_out_ivars_ = _excluded_out_ivars_.union(InterfaceObjectIO._excluded_out_ivars_)

    _ext_iface_upper_bound = INamedFile

    def _remove(self, m, *args):
        return [m.pop(x, None) for x in args]

    def toExternalObject(self, unused_mergeFrom=None, **kwargs):
        context = self._ext_replacement()
        contentType = getattr(context, 'contentType', None) or DEFAULT_CONTENT_TYPE
        self._remove(kwargs, 'name', 'decorate')
        adapter = IInternalObjectExternalizer(context, None)
        if adapter is not None:
            # pylint: disable=too-many-function-args
            result = adapter.toExternalObject(decorate=False, **kwargs)
        else:
            result = super(_FileExporter, self).toExternalObject(decorate=False, **kwargs)
            result['contentType'] = text_(contentType)
            decorateMimeType(context, result)
        result['url'] = encode(context.data, text_(contentType))
        self._remove(result, OID, NTIID)
        return result
