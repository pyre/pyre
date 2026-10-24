#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a uri can be extended with text, and that anything else is refused the python way
"""


def test() -> None:
    """
    Add text, and something that is not text, to a uri
    """
    # the home of the parser
    from pyre.primitives import uri

    # extend a uri with text
    assert str(uri.parse("file:/tmp") + "/a") == "file:/tmp/a"
    # attempt to
    try:
        # add a number
        uri.parse("file:/tmp") + 5
        # which should be unreachable
        assert False, "unreachable"
    # if python refuses, as it does with operands it cannot add
    except TypeError as error:
        # check that it is the usual complaint, not one about raising something odd
        assert "unsupported operand" in str(error)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
