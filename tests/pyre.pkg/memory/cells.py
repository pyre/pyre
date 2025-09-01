#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import itertools


# the driver
def intCells() -> None:
    """
    Sanity test: make sure the bindings for integral type cells
    """
    # access the cell types
    from pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # integral types
    signs = ["", "u"]
    sizes = [8, 16, 32, 64]

    # build the integral type names
    for perm, sign, size in itertools.product(const, signs, sizes):
        # assemble the python name of the cell
        name = f"{sign}int{size}{perm}"
        # assemble the name the cell reports
        cellName = f"{sign.upper()}Int{size}{perm}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert perm == ("" if cell.mutable else "Const")

    # all done
    return


def floatCells() -> None:
    """
    Sanity test: make sure the bindings for float type cells
    """
    # access the cell types
    from pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # float types
    sizes = [("float", 32), ("double", 64)]

    # build the integral type names
    for perm, (marker, size) in itertools.product(const, sizes):
        # assemble the name in the module
        name = f"{marker}{perm}"
        # assemble the name the cell reports
        cellName = f"{marker.capitalize()}{perm}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert perm == ("" if cell.mutable else "Const")

    # all done
    return


def complexCells() -> None:
    """
    Sanity test: make sure the bindings for complex type cells
    """
    # access the cell types
    from pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # float types
    sizes = [
        ("complexFloat", "ComplexFloat", 64),
        ("complexDouble", "ComplexDouble", 128),
    ]

    # build the integral type names
    for perm, (marker, tag, size) in itertools.product(const, sizes):
        # assemble the name in the module
        name = f"{marker}{perm}"
        # assemble the name the cell reports
        cellName = f"{tag}{perm}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert perm == ("" if cell.mutable else "Const")

    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    intCells()
    floatCells()
    complexCells()


# end of file
