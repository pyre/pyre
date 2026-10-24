#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an empty map is not a uri
"""


def test() -> None:
    """
    Convert an empty map
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.uri()

    # each of these
    for value in ({}, dict()):
        # attempt to
        try:
            # convert it
            schema.coerce(value)
            # which should be unreachable
            assert False, value
        # if it is refused, as expected
        except schema.CastingError:
            # all good
            pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
