#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from nti.namedfile import monkey as plonefile_zopefile_patch_on_import
plonefile_zopefile_patch_on_import.patch()

from zope import interface

from plone.namedfile.interfaces import IFile as IPloneFile
from plone.namedfile.interfaces import INamedFile as IPloneNamedFile
from plone.namedfile.interfaces import INamedImage as IPloneNamedImage
from plone.namedfile.interfaces import INamedBlobFile as IPloneNamedBlobFile
from plone.namedfile.interfaces import INamedBlobImage as IPloneNamedBlobImage

from nti.base.interfaces import IConstrained
from nti.base.interfaces import ILastModified

from nti.mimetype.mimetype import rfc2047MimeTypeConstraint

from nti.schema.field import Int
from nti.schema.field import ValidTextLine
from nti.schema.field import IndexedIterable
from nti.schema.field import ValidText as Text
from nti.schema.field import DecodingValidTextLine


class IFileConstraints(interface.Interface):

    allowed_mime_types = IndexedIterable(title=u"Mime types that are accepted",
                                         min_length=1,
                                         value_type=Text(title=u"An allowed mimetype",
                                                         constraint=rfc2047MimeTypeConstraint),
                                         default=[u'*/*'])

    allowed_extensions = IndexedIterable(title=u"Extensions like '.doc' that are accepted",
                                         min_length=0,
                                         value_type=Text(title=u"An allowed extension"),
                                         required=False,
                                         default=[u'*'])

    max_file_size = Int(title=u"Maximum size in bytes for the file",
                        min=1,
                        required=False)

    max_total_file_size = Int(title=u"Maximum size in bytes for all file attachments",
                              min=1,
                              required=False)

    max_files = Int(title=u"max attachments files", required=False, default=2)

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


class IFileConstrained(IConstrained):
    """
    Marker interface for objects that have associated :class:`.IFileConstraints`
    """

# For legacy purposes do not make IFile to be an ICreated object to avoid
# denying access due to default acl providers on ICreated objects. We need a
# default ACL provider for IFile objects


class IFile(IPloneFile, ILastModified):

    name = ValidTextLine(title=u"Identifier for the file",
                         required=False,
                         default=None)

    contentType = DecodingValidTextLine(title=u'Content type',
                                        required=False,
                                        default='',
                                        missing_value='')


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
    reference = ValidTextLine(title=u"the internal identifier",
                              required=False)
