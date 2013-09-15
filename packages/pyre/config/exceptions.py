# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError, BadResourceLocatorError


class ConfigurationError(FrameworkError):
    """
    Base class for all configuration errors
    """


class CodecError(ConfigurationError):
    """
    Base class for codec errors
    """

    def __init__(self, codec, uri="", description="generic codec error", **kwds):
        super().__init__(description=description, **kwds)
        self.codec = codec
        self.uri = uri
        return


class UnknownEncodingError(CodecError):
    """
    A request for an unknown codec was made
    """

    def __init__(self, encoding, **kwds):
        description = '{0.uri.uri!r}: unknown encoding {0.encoding!r}'
        super().__init__(codec=None, description=description, **kwds)
        self.encoding = encoding
        return


class DecodingError(CodecError):
    """
    Exception raised by codecs when they encounter errors in their input streams
    """

    
class EncodingError(CodecError):
    """
    Exception raised by codecs when they fail to inject an item in a stream
    """


class LoadingError(CodecError):
    """
    Exception raised by codecs when they encounter errors in their input streams
    """

    
class ShelfError(ConfigurationError):

    def __init__(self, shelf, **kwds):
        super().__init__(**kwds)
        self.shelf = shelf
        return
                 

class SymbolNotFoundError(ShelfError):

    def __init__(self, symbol, **kwds):
        msg = "symbol {0.symbol!r} not found in {0.shelf!r}"
        super().__init__(description=msg, **kwds)
        self.symbol = symbol
        return
                 

# end of file
