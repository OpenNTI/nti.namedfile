#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
    from nti.coremetadata.mixins import CreatedAndModifiedTimeMixin
except ImportError:
    from nti.namedfile._mixins import CreatedAndModifiedTimeMixin
CreatedAndModifiedTimeMixin = CreatedAndModifiedTimeMixin
