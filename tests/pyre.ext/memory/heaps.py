#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import itertools


# the driver
def heaps():
    """
    Verify that the heap expansions are all present
    """
    # get the module
    from pyre.extensions.pyre.memory import heaps

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
        f"{permission}Heap{type}"
        for permission, type in itertools.product(permissions, types)
    ]
    # go through them
    for name in names:
        # and verify they are all present
        assert getattr(heaps, name)

    # all done
    return


# main
if __name__ == "__main__":
    heaps()


# end of file
