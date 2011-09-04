#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""


def test():

    from pyre.algebraic.exceptions import NodeError, CircularReferenceError

    try:
        raise NodeError(description="generic error")
    except NodeError as error:
        pass

    try:
        raise CircularReferenceError(node=None, path=None)
    except CircularReferenceError as error:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
