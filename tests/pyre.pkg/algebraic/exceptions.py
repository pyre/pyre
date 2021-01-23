#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Tests for all exceptions raised by this package
    """

    # pull the exceptions
    from pyre.algebraic.exceptions import NodeError, CircularReferenceError

    # the base exception
    try:
        # raise it
        raise NodeError()
    # catch it
    except NodeError as error:
        # all good
        pass

    # circular references
    try:
        # raise it
        raise CircularReferenceError(node=None, path=None)
    # catch it
    except CircularReferenceError as error:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
