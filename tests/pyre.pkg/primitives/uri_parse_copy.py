#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that filling in the missing parts of a uri leaves the original alone
"""


def test() -> None:
    """
    Parse an existing uri with defaults for its missing parts
    """
    # the home of the parser
    from pyre.primitives import uri

    # a uri without a scheme
    original = uri.parse("/tmp/a")
    # filled in with one
    filled = uri.parse(original, scheme="file")
    # has it
    assert filled.scheme == "file"
    # while the original does not
    assert original.scheme is None
    # a default never replaces a part that is there
    assert uri.parse(filled, scheme="vfs").scheme == "file"
    # and a uri that has a scheme, an authority and an address comes back as it is
    complete = uri.parse("file://host/tmp/a")
    # when parsed again
    assert uri.parse(complete, scheme="vfs") is complete

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
