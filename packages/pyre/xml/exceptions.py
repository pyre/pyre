# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from . import newLocator
from ..framework.exceptions import FrameworkError


class ParsingError(FrameworkError):
    """
    Base class for parsing errors
    """

    def __init__(self, parser=None, document=None, locator=None, **kwds):
        super().__init__(**kwds)
        self.parser = parser
        self.document = document
        self.locator = newLocator(locator) if locator else None
        return

    def __str__(self):
        if self.locator:
            return "{0}: {1}".format(str(self.locator), self.description)

        return self.description


class UnsupportedFeatureError(ParsingError):
    """
    Exception raised when one of the requested features is not supported by the parser
    """

    def __init__(self, features, **kwds):
        msg = "unsupported features: {0!r}".format(", ".join(features))
        super().__init__(description=msg, **kwds)
        self.features = features
        return


class DTDError(ParsingError):
    """
    Errors relating to the structure of the document
    """


class ProcessingError(ParsingError):
    """
    Errors relating to the handling of the document
    """


# end of file 
