#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import itertools


# the driver
def maps():
    """
    Verify that the map expansions are all present
    """
    # get the module
    from pyre.extensions.pyre.memory import maps

    # given access rights
    permissions = ["", "Const"]
    # and basic types
    types = [
        # ints
        "Int8",
        "Int16",
        "Int32",
        "Int64",
        "UInt8",
        "UInt16",
        "UInt32",
        "UInt64",
        # floats
        "Float",
        "Double",
        # complex
        "ComplexFloat",
        "ComplexDouble",
    ]
    # build all possible names
    names = [
        f"Map{type}{permission}"
        for permission, type in itertools.product(permissions, types)
    ]
    # go through them
    for name in names:
        # and verify they are all present
        assert getattr(maps, name)

    # all done
    return


# main
if __name__ == "__main__":
    maps()


# end of file
