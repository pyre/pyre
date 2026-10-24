#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that numbers are uris of their text, since a resource may be named after one
"""


def test() -> None:
    """
    Convert numbers, and things that are not text or numbers
    """
    # the schemata
    import pyre.schemata
    import pyre.primitives

    # make a converter
    schema = pyre.schemata.uri()

    # an integer
    assert schema.coerce(5).address == "5"
    # a float
    assert schema.coerce(2.5).address == "2.5"
    # a path, which is text too
    assert schema.coerce(pyre.primitives.path("/tmp/a")).address == "/tmp/a"

    # each of these
    for value in (True, ["a", "b"], ("a",), {"a"}, object()):
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
