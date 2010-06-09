# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Definitions for the exceptions raised by this package
"""


# exceptions
from ..framework.exceptions import FrameworkError


class ParsingError(FrameworkError):
    """
    Base class for parsing exceptions

    Can be used to catch all exceptions raised by this package
    """

    def __init__(self, description, locator, **kwds):
        super().__init__(**kwds)
        self.description = description
        self.locator = locator
        return

    def __str__(self):
        return "error while parsing {0.locator}: {0.description}".format(self)


class TokenizationError(ParsingError):
    """
    Exception raised when the scanner fails to extract a token from the input stream
    """

    def __init__(self, text, **kwds):
        super().__init__(description="could not match {0!r}".format(text), **kwds)
        self.text = text
        return


# end of file 
