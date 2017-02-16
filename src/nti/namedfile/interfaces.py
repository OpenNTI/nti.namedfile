#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.namedfile import monkey as plonefile_zopefile_patch_on_import
plonefile_zopefile_patch_on_import.patch()

from zope import interface

from plone.namedfile.interfaces import IFile as IPloneFile
from plone.namedfile.interfaces import INamedFile as IPloneNamedFile
from plone.namedfile.interfaces import INamedImage as IPloneNamedImage
from plone.namedfile.interfaces import INamedBlobFile as IPloneNamedBlobFile
from plone.namedfile.interfaces import INamedBlobImage as IPloneNamedBlobImage

from nti.base.interfaces import ILastModified

from nti.mimetype.mimetype import mimeTypeConstraint

from nti.schema.field import Int
from nti.schema.field import ValidTextLine
from nti.schema.field import IndexedIterable
from nti.schema.field import ValidText as Text


class IFileConstraints(interface.Interface):

    allowed_mime_types = IndexedIterable(title="Mime types that are accepted",
                                         min_length=1,
                                         value_type=Text(title="An allowed mimetype",
                                                         constraint=mimeTypeConstraint),
                                         default=['*/*'])

    allowed_extensions = IndexedIterable(title="Extensions like '.doc' that are accepted",
                                         min_length=0,
                                         value_type=Text(title="An allowed extension"),
                                         required=False,
                                         default=['*'])

    max_file_size = Int(title="Maximum size in bytes for the file",
                        min=1,
                        required=False)

    max_files = Int(title="max attachments files", required=False, default=2)

    def is_file_size_allowed(size=None):
        """
        Return whether or not the given size is allowed
        """

    def is_mime_type_allowed(mime_type=None):
        """
        Return whether or not the given mime type, which must match
        the mime type constraint, is one of the allowed types of this
        part, taking into account wildcards.
        """

    def is_filename_allowed(filename=None):
        """
        Return whether the filename given is allowed according to
        the allowed list of extensions (case-insensitive).
        """


class IFileConstrained(interface.Interface):
    """
    Marker interface for objects that have associated :class:`.IFileConstraints`
    """

# XXX: For legacy purposes do not make IFile to be an ICreated object to avoid
# denying access due to default acl providers on ICreated objects. We need a
# default ACL provider for IFile objects


class IFile(IPloneFile, ILastModified):
    name = ValidTextLine(title="Identifier for the file",
                         required=False,
                         default=None)


class INamedFile(IFile, IPloneNamedFile):
    pass


class INamedImage(IFile, IPloneNamedImage):
    pass


class INamedBlobFile(IPloneNamedBlobFile, INamedFile):
    pass


class INamedBlobImage(IPloneNamedBlobImage, INamedImage):
    pass


class IInternalFileRef(interface.Interface):
    """
    Marker interface for reference to an internal file
    """
    reference = ValidTextLine(title="the internal identifier", 
                              required=False)
