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

    def __init__(self, codec, uri, locator, **kwds):
        super().__init__(**kwds)
        self.codec = codec
        self.uri = uri
        self.locator = locator
        return


class DecodingError(CodecError):
    """
    Exception raised by codecs when they encounter errors in their input streams
    """

    def __str__(self):
        return "decoding error"

    
class EncodingError(CodecError):
    """
    Exception raised by codecs when they fail to inject an iterm in a stream
    """

    def __str__(self):
        return "encoding error"


# end of file
