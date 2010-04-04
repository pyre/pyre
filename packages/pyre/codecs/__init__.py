# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This package contains the implementation of the readers and writers of the various
configuration file formats supported by pyre.

"""


# factory
def newManager(**kwds):
    from .CodecManager import CodecManager
    return CodecManager(**kwds)


# exceptions
from ..framework import FrameworkError


class CodecError(FrameworkError):
    """
    Base class for codec errors
    """

    def __init__(self, codec, uri, locator, description, **kwds):
        super().__init__(**kwds)
        self.codec = codec
        self.uri = uri
        self.locator = locator
        self.description = description
        return

    def __str__(self):
        return self.description


class DecodingError(CodecError):
    """
    Exception raised by codecs when they encounter errors in their input streams
    """

    
class EncodingError(CodecError):
    """
    Exception raised by codecs when they fail to inject an iterm in a stream
    """


# end of file
