#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import unittest

from zope.dottedname import resolve as dottedname


class TestUtils(unittest.TestCase):

    def test_import_utils(self):
        dottedname.resolve('nti.namedfile.utils')
