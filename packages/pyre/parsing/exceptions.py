# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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


class TokenizationError(ParsingError):
    """
    Exception raised when the scanner fails to extract a token from the input stream
    """

    def __init__(self, text, **kwds):
        super().__init__(description="could not match {0.text!r}", **kwds)
        self.text = text
        return


class SyntaxError(ParsingError):
    """
    Exception raised when a syntax error is detected
    """

    def __init__(self, token, **kwds):
        super().__init__(description="syntax error: {0.token.lexeme!r}", **kwds)
        self.token = token
        return


# end of file
