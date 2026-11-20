#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an enum writes the name of its member, which reads back as the same member
"""


def test() -> None:
    """
    Write a member of an enumeration and read it back
    """
    # support
    import enum
    import pyre

    # an enumeration
    class Color(enum.Enum):
        """
        Some colors
        """

        # the members
        red = 1
        # and another
        green = 2

    # make a schema
    schema = pyre.schemata.enum(enum=Color)

    # a member writes its name
    assert schema.string(Color.green) == "green", schema.string(Color.green)
    # which reads back as the same member
    assert schema.coerce(value=schema.string(Color.green)) is Color.green
    # and {None} is left alone
    assert schema.string(None) is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
