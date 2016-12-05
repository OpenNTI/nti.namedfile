#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import time

class CreatedTimeMixin(object):

    _SET_CREATED_MODTIME_ON_INIT = True

    createdTime = 0

    def __init__(self, *args, **kwargs):
        if self._SET_CREATED_MODTIME_ON_INIT and self.createdTime == 0:
            self.createdTime = time.time()
        super(CreatedTimeMixin, self).__init__(*args, **kwargs)

class ModifiedTimeMixin(object):

    lastModified = 0

    def __init__(self, *args, **kwargs):
        super(ModifiedTimeMixin, self).__init__(*args, **kwargs)

    def updateLastMod(self, t=None):
        now = time.time()
        self.lastModified = (t if t is not None and t > self.lastModified else now)
        return self.lastModified

    def updateLastModIfGreater(self, t):
        if t is not None and t > self.lastModified:
            self.lastModified = t
        return self.lastModified
    
class CreatedAndModifiedTimeMixin(CreatedTimeMixin, ModifiedTimeMixin):

    def __init__(self, *args, **kwargs):
        if self._SET_CREATED_MODTIME_ON_INIT:
            self.createdTime = time.time()
            self.updateLastModIfGreater(self.createdTime)
        super(CreatedAndModifiedTimeMixin, self).__init__(*args, **kwargs)
