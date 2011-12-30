#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():

    from pyre.parsing.exceptions import (
        ParsingError, TokenizationError
        )

    try:
        raise ParsingError(description=None, locator=None)
    except ParsingError as error:
        pass

    try:
        raise TokenizationError(text=None, locator=None)
    except TokenizationError as error:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
