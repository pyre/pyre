#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a cell writes its full name, which reads back as the same cell
"""


def test() -> None:
    """
    Write a few cells and read them back
    """
    # support
    import pyre

    # make a schema
    schema = pyre.schemata.cell()
    # the cells
    cells = pyre.memory.cells

    # each cell, and the name it writes
    cases = [
        (cells.uint8, "uint8"),
        (cells.int32, "int32"),
        (cells.double, "float64"),
        (cells.complexFloat, "complex64"),
        (cells.doubleConst, "const float64"),
    ]
    # go through them
    for cell, name in cases:
        # the cell writes its full name
        assert schema.string(cell) == name, (name, schema.string(cell))
        # which reads back as the same cell
        assert schema.coerce(value=name) is cell, name

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
