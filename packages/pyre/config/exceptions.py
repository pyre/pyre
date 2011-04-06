# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError


class ConfigurationError(FrameworkError):
    """
    Base class for all configuration errors
    """


class CodecError(ConfigurationError):
    """
    Base class for codec errors
    """

    def __init__(self, codec, uri="", locator=None, description=" generic codec error", **kwds):
        super().__init__(description=description, **kwds)
        self.codec = codec
        self.uri = uri
        self.locator = locator
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


class ShelfError(ConfigurationError):

    def __init__(self, shelf, **kwds):
        msg = "generic shelf error: {!r}".format(shelf)
        super().__init__(description=msg, **kwds)
        self.shelf = shelf
        return
                 

class SymbolNotFoundError(ShelfError):

    def __init__(self, shelf, symbol, **kwds):
        msg = "symbol {!r} not found in {!r}".format(symbol, shelf)
        super().__init__(description=msg, shelf=shelf, **kwds)
        self.symbol = symbol
        return
                 


# end of file
